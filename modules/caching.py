from pandas import read_csv
import pandas as pd
import time

def cache(func, output_path="./caches"):
    FUNCTION_NAME = func.__name__
    def wrapper(*args, **kwargs):
        CSV_PATH = f"{output_path}/{FUNCTION_NAME}.csv"
        all_args = kwargs.copy()
        for i, x in enumerate(args):
            all_args[f"__{i}"] = x
        
        df = None
        # Reads CSV
        try:
            df = read_csv(CSV_PATH)
            df["__cached_ans"]
        except:
            all_args["__cached_ans"] = None
            
            df = {x: [] for x in all_args.keys()}
            pd.DataFrame(df).to_csv(CSV_PATH, index=False)
        try:
            for i in range(len(df["__cached_ans"])):
                for key in all_args:
                    if str(df[key][i]) != str(all_args[key]):
                        break
                    return df["__cached_ans"][i]
                for key in all_args:
                    if df[key][i] != all_args[key]:
                        break
                    return df["__cached_ans"][i]
        except KeyError:
            for key in all_args:
                if key not in df:
                    df[key] = [None] * len(df["__cached_ans"])
                    df[key][0] = key
            
            
            

        # Writes CSV
        ans = func(*args, **kwargs)
        all_args["__cached_ans"] = ans
        df = pd.concat([df, pd.DataFrame({x: [all_args[x]] for x in all_args.keys()})])

        
        

        df.to_csv(CSV_PATH, index=False, mode="w")
        return ans

    return wrapper


if __name__ == "__main__":
    @cache
    def test(x):
        print("calc...")
        time.sleep(5)
        return x


    print(test(x=3))
    print(test(x=2))
    print(test(x=5))
    print(test(x=6))
    print(test(6))
    print(test(3))