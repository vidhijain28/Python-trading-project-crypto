from dataclasses import dataclass,field
import heapq,itertools,random
_counter=itertools.count()
@dataclass(order=True)
class PrioritizedOrder:
    priority:float; sequence:int; order:dict=field(compare=False)
class OrderBook:
    def __init__(self,symbol): self.symbol=symbol; self.bids=[]; self.asks=[]; self.orders={}
    def add_order(self,order):
        oid=order.get('order_id') or f'{self.symbol}_{next(_counter)}'; order['order_id']=oid; seq=next(_counter); price=float(order['price'])
        heapq.heappush(self.bids if order['side']=='BUY' else self.asks, PrioritizedOrder(-price if order['side']=='BUY' else price,seq,order)); self.orders[oid]=order; return oid
    def cancel_order(self,oid):
        if oid in self.orders: self.orders[oid]['status']='CANCELLED'; return True
        return False
    def best_bid(self):
        while self.bids and self.bids[0].order.get('status')=='CANCELLED': heapq.heappop(self.bids)
        return None if not self.bids else self.bids[0].order
    def best_ask(self):
        while self.asks and self.asks[0].order.get('status')=='CANCELLED': heapq.heappop(self.asks)
        return None if not self.asks else self.asks[0].order
class OrderManager:
    def __init__(self,initial_cash,max_position_pct=0.25,max_gross_exposure=1.0): self.initial_cash=initial_cash; self.max_position_pct=max_position_pct; self.max_gross_exposure=max_gross_exposure
    def validate(self,order,cash,positions,prices):
        sym=order['symbol']; qty=float(order['qty']); price=float(order['price']); notional=qty*price; pv=cash+sum(positions.get(s,0.0)*px for s,px in prices.items())
        if order['side']=='BUY' and notional>cash: return False,'Insufficient cash'
        if order['side']=='BUY' and abs(positions.get(sym,0.0)*price)+notional>self.max_position_pct*pv: return False,'Position limit exceeded'
        return True,'OK'
class MatchingEngine:
    def __init__(self,taker_fee_bps=7.5,slippage_bps=2.5,partial_fill_probability=0.10): self.taker_fee_bps=taker_fee_bps; self.slippage_bps=slippage_bps; self.partial_fill_probability=partial_fill_probability
    def execute_market_order(self,order):
        side=order['side']; price=float(order['price']); qty=float(order['qty']); px=price*(1+self.slippage_bps/10000 if side=='BUY' else 1-self.slippage_bps/10000)
        if random.random()<self.partial_fill_probability: fill=qty*random.uniform(0.3,0.9); status='PARTIAL_FILL'
        else: fill=qty; status='FILLED'
        fee=abs(fill*px)*self.taker_fee_bps/10000
        return {'timestamp':order['timestamp'],'symbol':order['symbol'],'side':side,'requested_qty':qty,'filled_qty':fill,'price':price,'execution_price':px,'fee':fee,'status':status,'order_id':order.get('order_id')}
