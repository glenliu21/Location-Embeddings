import pandas as pd

# Read in DMA data
dma_df = pd.read_csv("s3://ojo-data-science/scratch/kentcz/states/market-zipcodes.csv",
                         dtype={"zipcode": str},
                         usecols=["dma", "zipcode"])
# Only get US zipcodes
dma_df["zip_length"] = dma_df["zipcode"]
dma_df["zip_length"] = dma_df["zip_length"].apply(lambda x: len(x))
dma_df = dma_df[dma_df["zip_length"] == 5]
dma_df.drop("zip_length", axis=1, inplace=True)
dma_df.reset_index(drop=True, inplace=True)

# Generate zipcode-dma hashtable
zipcode_hash = dict()
for _, row in dma_df.iterrows():
    zipcode_hash[row["zipcode"]] = row["dma"]
    
# Get the DMA of a zipcode or sentence of zipcodes (assumption is that all zipcodes in that sentence are in same DMA)
def get_dma(zipcode):
    # Empty input
    if len(zipcode) == 0:
        return None
    elif type(zipcode) == str:
        try:
            dma = zipcode_hash[zipcode]
            return dma
        except:
            return None
    elif type(zipcode) == list:
        try:
            dma = zipcode_hash[zipcode[0]]
            return dma
        except:
            return None
    else:
        print("invalid type for get_dma")
        return None
    
# Generate DMA -> zipcodes hashtable
dma_zipcode_hash = dict()
for _, row in dma_df.iterrows():
    current_dma = get_dma(row["zipcode"])
    zipcodes = dma_df[dma_df["dma"] == current_dma].zipcode.values
    dma_zipcode_hash[current_dma] = zipcodes
    
# Get zipcodes in a DMA
def get_dma_zipcodes(dma):
    if dma in dma_zipcode_hash:
        return dma_zipcode_hash[dma]
    else:
        return None
    
    
    