from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
Key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,Key)

data = supabase.table('todos').insert({'name': 'jose'}).execute()


data = supabase.table('todos').select ('*').execute()
print(data) 

