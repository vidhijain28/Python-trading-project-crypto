from dataclasses import dataclass
@dataclass
class MultiCryptoMomentumStrategy:
    long_threshold:float=0.80; exit_threshold:float=0.55; max_symbols:int=2; base_order_notional:float=10_000.0
    def generate_signals_at_time(self,market_slice):
        df=market_slice.copy(); df['signal']='HOLD'; top=df[df['signal_rank']>=self.long_threshold].sort_values('signal_rank',ascending=False).head(self.max_symbols)['symbol']
        df.loc[df['symbol'].isin(set(top)),'signal']='BUY'; df.loc[df['signal_rank']<self.exit_threshold,'signal']='SELL'
        return df[['Datetime','symbol','Close','signal','signal_rank','vol_288']]
    def generate_orders(self,market_slice,positions,cash):
        orders=[]; sig=self.generate_signals_at_time(market_slice)
        for _,r in sig.iterrows():
            sym=r.symbol; price=float(r.Close); s=r.signal
            if s=='BUY' and positions.get(sym,0.0)<=0:
                notional=min(self.base_order_notional,cash*0.20); qty=notional/price
                if qty>0: orders.append({'timestamp':r.Datetime,'symbol':sym,'side':'BUY','qty':qty,'price':price,'order_type':'MARKET'})
            elif s=='SELL' and positions.get(sym,0.0)>0:
                orders.append({'timestamp':r.Datetime,'symbol':sym,'side':'SELL','qty':positions[sym],'price':price,'order_type':'MARKET'})
        return orders
