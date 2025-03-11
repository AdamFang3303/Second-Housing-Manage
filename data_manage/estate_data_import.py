from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import text
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/sh_housing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 EstateInfo 模型
class EstateInfo(db.Model):
    __tablename__ = 'estate_info'
    id = db.Column(db.Integer, primary_key=True)
    estate_name = db.Column(db.String(255), nullable=False)
    average_price = db.Column(db.Integer, nullable=False)
    listings = db.Column(db.Integer, nullable=False)
    district = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

# 重置自增 ID
def reset_auto_increment():
    db.session.execute(text("ALTER TABLE house_info AUTO_INCREMENT = 1"))
    db.session.commit()

# 导入 CSV 文件
def import_csv_to_mysql(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 跳过表头

        for row in csv_reader:
            estate_name, average_price_str, listings, district, street, longitude, latitude = row
            
            # 去掉 estate_name 前后的换行符
            estate_name = estate_name.strip()
            
            # 检查 average_price_str 是否为有效的数字字符串
            if average_price_str.strip() == '暂无数据' or not average_price_str.strip() or average_price_str.strip() == '0' or average_price_str.strip() == '均价':
                average_price = None
            else:
                average_price = int(average_price_str)
            
            # 如果 average_price 为 None，跳过该行
            if average_price is None:
                print(f"Skipping row due to invalid price: {row}")
                continue
            
            estate_info = EstateInfo(
                estate_name=estate_name,
                average_price=average_price,
                listings=int(listings),
                district=district,
                street=street,
                longitude=float(longitude),
                latitude=float(latitude)
            )
            db.session.add(estate_info)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        reset_auto_increment()  # 重置自增 ID
        import_csv_to_mysql('./data/杭州小区数据_带坐标.csv')
        print("导入完成")
    app.run(debug=False)