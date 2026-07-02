import numpy as np, pandas as pd
from .config import CLEAN_DIR,FEATURE_DIR

def clean_market_data(raw):
    req={'Datetime','symbol','Open','High','Low','Close','Volume'}; miss=req.difference(raw.columns)
    if miss: raise KeyError(f'Missing required columns: {miss}. Available: {list(raw.columns)}')
    df=raw.copy(); df['Datetime']=pd.to_datetime(df['Datetime'],utc=True); df=df.drop_duplicates(['symbol','Datetime']).dropna(subset=list(req))
    for c in ['Open','High','Low','Close','Volume']: df[c]=pd.to_numeric(df[c],errors='coerce')
    return df.dropna(subset=['Open','High','Low','Close','Volume']).sort_values(['symbol','Datetime']).reset_index(drop=True)

def engineer_features(clean):
    df=clean.copy().sort_values(['symbol','Datetime']); g=df.groupby('symbol',group_keys=False)
    df['ret_5m']=g['Close'].pct_change(); df['log_ret_5m']=g['Close'].transform(lambda s: np.log(s).diff())
    df['momentum_12']=g['Close'].pct_change(12); df['momentum_48']=g['Close'].pct_change(48); df['momentum_288']=g['Close'].pct_change(288)
    df['ma_24']=g['Close'].transform(lambda s:s.rolling(24).mean()); df['ma_96']=g['Close'].transform(lambda s:s.rolling(96).mean()); df['ma_spread']=df['ma_24']/df['ma_96']-1
    df['vol_48']=g['log_ret_5m'].transform(lambda s:s.rolling(48).std()); df['vol_288']=g['log_ret_5m'].transform(lambda s:s.rolling(288).std())
    df['volume_z_288']=g['Volume'].transform(lambda s:(s-s.rolling(288).mean())/s.rolling(288).std())
    df['cs_momentum_rank']=df.groupby('Datetime')['momentum_48'].rank(pct=True); df['cs_vol_rank']=df.groupby('Datetime')['vol_288'].rank(pct=True)
    df['raw_signal']=0.5*df['cs_momentum_rank']+0.3*df['ma_spread'].rank(pct=True)-0.2*df['cs_vol_rank']
    df['signal_rank']=df.groupby('Datetime')['raw_signal'].rank(pct=True); df['target_next_ret']=g['ret_5m'].shift(-1)
    return df.dropna().reset_index(drop=True)

def save_clean_and_features(clean,features,tag='latest'):
    cp=CLEAN_DIR/f'multi_crypto_clean_{tag}.parquet'; fp=FEATURE_DIR/f'multi_crypto_features_{tag}.parquet'
    clean.to_parquet(cp,index=False); features.to_parquet(fp,index=False); return cp,fp

def load_latest_features():
    files=sorted(FEATURE_DIR.glob('multi_crypto_features_*.parquet'))
    if not files: raise FileNotFoundError(f'No feature parquet files found in {FEATURE_DIR}. Run notebooks 01 and 02 first.')
    return pd.read_parquet(files[-1])
