import os
import time
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",  
    api_key=os.environ["HF_TOKEN"],
)

# Retry
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((Exception,)),
)

def translate_text(text):
    model_name = "openai/gpt-oss-120b:fastest"
    
    system_prompt = """You are a professional academic translator specializing in computer vision and machine learning papers. 
Translate the following English text into Chinese. Requirements:
1. Maintain academic tone and technical accuracy
2. Ensure the translation is fluent and natural in Chinese
3. Only output the translated text, no explanations"""
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3,  
            max_tokens=2048,   
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\nError: {e}")
        raise 


def load_checkpoint(checkpoint_file="checkpoint.csv"):
    if os.path.exists(checkpoint_file): 
        try:
            df_checkpoint = pd.read_csv(checkpoint_file)
            return df_checkpoint
        except Exception as e:
            print(f"Warning: Could not load checkpoint: {e}")
            return None
    return None


def main():
    input_file = "iccv2025.csv"
    output_file = "result.csv"
    checkpoint_file = "checkpoint.csv"
    
    df = pd.read_csv(input_file)
    
    # Try to load checkpoint
    df_checkpoint = load_checkpoint(checkpoint_file)
    start_index = 0
    
    if df_checkpoint is not None:
        print(f"Found checkpoint with {len(df_checkpoint)} completed translations")
        response = input("Resume from checkpoint? (y/n): ").strip().lower()
        if response == 'y':
            df = pd.concat([df_checkpoint, df.iloc[len(df_checkpoint):]], ignore_index=True)
            start_index = len(df_checkpoint)
            print(f"Resuming from row {start_index}")
    
    if 'title_cn' not in df.columns:
        df['title_cn'] = ''
    if 'abstract_cn' not in df.columns:
        df['abstract_cn'] = ''
    
    # Starting Translate 
    for index in tqdm(range(start_index, len(df)), desc="Translating papers"):
        row = df.iloc[index]
               
        try:
            if pd.notna(row['title']):
                title_cn = translate_text(row['title'])
                df.at[index, 'title_cn'] = title_cn
            
            if pd.notna(row['abstract']):
                abstract_cn = translate_text(row['abstract'])
                df.at[index, 'abstract_cn'] = abstract_cn
            # Save every 5 rows
            if (index + 1) % 5 == 0:
                df.iloc[:index+1].to_csv(checkpoint_file, index=False, encoding="utf-8")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"\nFailed to translate row {index} after retries: {e}")
            # Save what we have so far
            df.iloc[:index].to_csv(checkpoint_file, index=False, encoding="utf-8")
            print(f"Progress saved to checkpoint.")
            raise
    
    # Save all
    print(f"\nSaving results to {output_file}...")
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\nTranslation complete! Total papers: {len(df)}")



if __name__ == "__main__":
    main()