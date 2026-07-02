import time, requests, pandas as pd
from .config import BINANCE_BASE_URL,KLINES_ENDPOINT,RAW_DIR

def to_milliseconds(dt): return int(pd.Timestamp(dt,tz='UTC').timestamp()*1000)

def safe_get(url,params,max_retries=6,timeout=60):
    for a in range(max_retries):
        try:
            r=requests.get(url,params=params,timeout=timeout); r.raise_for_status(); return r
        except requests.exceptions.RequestException as e:
            wait=min(2**a,30); print(f'Request failed: {e}. Retrying in {wait}s...'); time.sleep(wait)
    raise RuntimeError(f'Max retries exceeded: {params}')

def fetch_klines(symbol,interval,start,end,limit=1000,sleep=0.25):
    url=BINANCE_BASE_URL+KLINES_ENDPOINT; start_ms=to_milliseconds(start); end_ms=to_milliseconds(end); rows=[]
    while start_ms<end_ms:
        params={'symbol':symbol,'interval':interval,'startTime':start_ms,'endTime':end_ms,'limit':limit}
        data=safe_get(url,params).json()
        if not data: break
        rows.extend(data); nxt=data[-1][0]+1
        if nxt<=start_ms: break
        start_ms=nxt; time.sleep(sleep)
    if not rows: return pd.DataFrame()
    cols=['open_time','Open','High','Low','Close','Volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_volume','taker_buy_quote_volume','ignore']
    df=pd.DataFrame(rows,columns=cols); df['Datetime']=pd.to_datetime(df['open_time'],unit='ms',utc=True); df['symbol']=symbol
    nums=['Open','High','Low','Close','Volume','quote_asset_volume','number_of_trades','taker_buy_base_volume','taker_buy_quote_volume']
    for c in nums: df[c]=pd.to_numeric(df[c],errors='coerce')
    keep=['Datetime','symbol','Open','High','Low','Close','Volume','quote_asset_volume','number_of_trades','taker_buy_base_volume','taker_buy_quote_volume']
    return df[keep].drop_duplicates(['symbol','Datetime']).sort_values(['symbol','Datetime'])

def download_symbol(symbol,interval,start,end):
    print(f'Downloading {symbol}...'); df=fetch_klines(symbol,interval,start,end)
    if df.empty: print(f'No data returned for {symbol}.'); return df
    out=RAW_DIR/f'{symbol}_{interval}_{start}_{end}.parquet'; df.to_parquet(out,index=False); print(f'Saved {symbol}: {df.shape} -> {out}'); return df

def load_raw_files():
    files=sorted(RAW_DIR.glob('*.parquet'))
    if not files: raise FileNotFoundError(f'No raw parquet files found in {RAW_DIR}. Run notebook 01 first.')
    return pd.concat([pd.read_parquet(f) for f in files],ignore_index=True)
