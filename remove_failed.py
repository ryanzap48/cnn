import pandas as pd

# Load your data
df = pd.read_csv('drug_interactions_with_smiles.csv')

print(f"Original dataset size: {len(df)} rows")

# List of drugs to remove
drugs_to_remove = [
    'Polythiazide',
    'Radium Ra 223 dichloride',
    'Verteporfin',
    'Sucralfate',
    'Kaolin',
    'Methadyl acetate',
    'Nitric Oxide',
    'Nitroprusside',
    'Pentosan polysulfate',
    'Mipomersen',
    'Polymyxin B'
]

# Remove rows where either Drug 1 or Drug 2 is in the removal list
df_cleaned = df[~df['Drug 1'].isin(drugs_to_remove) & ~df['Drug 2'].isin(drugs_to_remove)]

print(f"Cleaned dataset size: {len(df_cleaned)} rows")
print(f"Removed: {len(df) - len(df_cleaned)} rows")

# Save cleaned dataset
df_cleaned.to_csv('drug_interactions_cleaned.csv', index=False)
print("\nSaved: drug_interactions_cleaned.csv")

# Optional: Show which drugs were actually found and removed
for drug in drugs_to_remove:
    count = len(df[(df['Drug 1'] == drug) | (df['Drug 2'] == drug)])
    if count > 0:
        print(f"  - {drug}: {count} interactions removed")