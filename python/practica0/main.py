import os
from supabase import Client, create_client
from dotenv import load_dotenv
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
Key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,Key)

data = supabase.table('todos').select('*').execute()
print(data)

data = supabase.table('todos').select('*').execute()
print(data)

data = supabase.table('todos').select('*').execute()
print(data)

data = supabase.table('todos').select('*').execute()
print(data)

data = supabase.table('todos').select('*').execute()
print(data)
