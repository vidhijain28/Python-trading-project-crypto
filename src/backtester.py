import numpy as np, pandas as pd
from .execution import OrderManager,MatchingEngine
from .config import INITIAL_CASH,MAX_POSITION_PCT,MAX_GROSS_EXPOSURE,TAKER_FEE_BPS,SLIPPAGE_BPS
class EventDrivenBacktester:
    def __init__(self,data,strategy,initial_cash=INITIAL_CASH):
        self.data=data.sort_values(['Datetime','symbol']).copy(); self.strategy=strategy; self.cash=initial_cash; self.initial_cash=initial_cash; self.positions={}; self.trades=[]; self.equity_curve=[]
        self.order_manager=OrderManager(initial_cash,MAX_POSITION_PCT,MAX_GROSS_EXPOSURE); self.matching_engine=MatchingEngine(TAKER_FEE_BPS,SLIPPAGE_BPS)
    def mark_to_market(self,prices): return self.cash+sum(q*prices.get(s,0.0) for s,q in self.positions.items())
    def run(self,max_steps=None):
        groups=list(self.data.groupby('Datetime',sort=True)); groups=groups[:max_steps] if max_steps else groups
        for ts,sl in groups:
            prices=dict(zip(sl['symbol'],sl['Close'])); orders=self.strategy.generate_orders(sl,self.positions,self.cash)
            for o in orders:
                ok,reason=self.order_manager.validate(o,self.cash,self.positions,prices)
                if not ok: continue
                ex=self.matching_engine.execute_market_order(o); self.apply_execution(ex); self.trades.append(ex)
            self.equity_curve.append({'Datetime':ts,'equity':self.mark_to_market(prices),'cash':self.cash,'gross_exposure':sum(abs(self.positions.get(s,0.0)*px) for s,px in prices.items())})
        return pd.DataFrame(self.equity_curve),pd.DataFrame(self.trades)
    def apply_execution(self,ex):
        sym=ex['symbol']; side=ex['side']; qty=float(ex['filled_qty']); px=float(ex['execution_price']); fee=float(ex['fee']); notional=qty*px
        if side=='BUY': self.cash-=notional+fee; self.positions[sym]=self.positions.get(sym,0.0)+qty
        else: self.cash+=notional-fee; self.positions[sym]=self.positions.get(sym,0.0)-qty; self.positions[sym]=0.0 if abs(self.positions[sym])<1e-10 else self.positions[sym]
def compute_performance(eq):
    df=eq.copy(); df['returns']=df['equity'].pct_change().fillna(0); tr=df['equity'].iloc[-1]/df['equity'].iloc[0]-1; ppy=365*24*12
    ar=(1+tr)**(ppy/max(len(df),1))-1; av=df['returns'].std()*np.sqrt(ppy); sharpe=ar/av if av>0 else np.nan; dd=df['equity']/df['equity'].cummax()-1
    return {'total_return':tr,'annualized_return':ar,'annualized_volatility':av,'sharpe':sharpe,'max_drawdown':dd.min(),'final_equity':df['equity'].iloc[-1]}
