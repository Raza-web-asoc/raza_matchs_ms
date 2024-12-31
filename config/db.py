from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()
pospas = os.getenv('pospas')
# engine = create_engine("mysql+pymysql://root:PASSWORD@localhost:3306/test")
print(f"postgresql://postgres.csrnoewasyfysslyjdze:{pospas}@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
engine = create_engine(f"postgresql://postgres.csrnoewasyfysslyjdze:{pospas}@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
meta_data=MetaData()