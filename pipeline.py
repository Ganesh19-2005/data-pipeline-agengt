import pandas as pd
import time

def run_pipeline(file_path):
    logs = []   # store agent logs

    def log(step):
        print(step)
        logs.append(step)

    # 🔁 Retry function
    def retry(func, df=None, retries=2):
        for i in range(retries):
            try:
                return func(df) if df is not None else func()
            except Exception as e:
                log(f"Retry {i+1} failed: {e}")
                time.sleep(1)
        raise Exception("Step failed after retries")

    # STEP 1: LOAD
    log("🤖 Step 1: Loading data")
    df = retry(lambda: pd.read_csv(file_path))

    # STEP 2: CLEAN
    log("🧹 Step 2: Cleaning data")
    df = retry(lambda d: d.drop_duplicates(), df)
    df = df.ffill()

    # STEP 3: TRANSFORM
    log("🔄 Step 3: Transforming data")
    if 'age' in df.columns:
        df['age_plus_10'] = df['age'] + 10

    # STEP 4: VALIDATE
    log("✅ Step 4: Validating data")
    if df.empty:
        raise ValueError("Data is empty!")

    # STEP 5: STORE
    log("💾 Step 5: Saving data")
    df.to_csv("output.csv", index=False)

    return df, logs