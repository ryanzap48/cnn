import pandas as pd
import pubchempy as pcp
import time
from tqdm import tqdm

def get_smiles_robust(drug_name):
    """Get SMILES using pubchempy library (more reliable)"""
    try:
        # Search for compound
        results = pcp.get_compounds(drug_name, 'name')
        
        if results:
            # Get the first result
            compound = results[0]
            return compound.canonical_smiles
        else:
            return None
    except Exception as e:
        return None

# Load data
df = pd.read_csv('db_drug_interactions.csv')

# Get unique drugs
unique_drugs = pd.concat([df['Drug 1'], df['Drug 2']]).unique()
print(f"Total unique drugs: {len(unique_drugs)}")

# Test with first 20
test_drugs = unique_drugs

# Create SMILES lookup dictionary
smiles_dict = {}
successful = 0
failed = []

for drug in tqdm(test_drugs, desc="Fetching SMILES"):
    smiles = get_smiles_robust(drug)
    smiles_dict[drug] = smiles
    
    if smiles:
        successful += 1
        print(f"✓ {drug}: {smiles[:50]}...")
    else:
        failed.append(drug)
        print(f"✗ {drug}: Not found")


# Results summary
print(f"\n{'='*60}")
print(f"Success rate: {successful}/{len(test_drugs)} ({successful/len(test_drugs)*100:.1f}%)")
print(f"\nFailed drugs:")
for drug in failed:
    print(f"  - {drug}")
print(f"{'='*60}")

# Map to dataframe
df['Drug1_SMILES'] = df['Drug 1'].map(smiles_dict)
df['Drug2_SMILES'] = df['Drug 2'].map(smiles_dict)

# Save
df.to_csv('drug_interactions_with_smiles.csv', index=False)
print("\nSaved: drug_interactions_with_smiles.csv")


"""
not able to get smiles for 
  - Polythiazide
  - Radium Ra 223 dichloride
  - Verteporfin
  - Sucralfate
  - Kaolin
  - Methadyl acetate
  - Nitric Oxide
  - Nitroprusside
  - Pentosan polysulfate
  - Mipomersen
  - Polymyxin B
"""