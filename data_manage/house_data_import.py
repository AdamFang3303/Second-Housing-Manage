from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import text
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/sh_housing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 HouseInfo 模型
class HouseInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_info_link = db.Column(db.String(255), nullable=False)
    house_address = db.Column(db.String(255), nullable=False)
    house_type = db.Column(db.String(50), nullable=False)
    house_area = db.Column(db.Float, nullable=False)
    orientation = db.Column(db.String(50), nullable=False)
    decoration = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)  # 允许 year 字段为 NULL
    house_category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    city = db.Column(db.String(50), nullable=False)

# 重置自增 ID
def reset_auto_increment():
    db.session.execute(text("ALTER TABLE house_info AUTO_INCREMENT = 1"))
    db.session.commit()

# 导入 CSV 文件
def import_csv_to_mysql(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 跳过表头

        # 打印 CSV 文件的总行数
        row_count = sum(1 for row in csv_reader)
        print(f"Total rows in CSV file: {row_count}")

        # 重新定位文件指针到开头
        csv_file.seek(0)
        next(csv_reader)  # 再次跳过表头

        # 逐行处理数据
        for row in csv_reader:
            house_info_link, house_address, house_type, house_area, orientation, decoration, floor, year_str, house_category, price, city = row
            # 检查 year_str 是否为有效的数字字符串
            if year_str.strip() == '暂无数据' or not year_str.strip():
                year = None
            else:
                year = int(year_str)
            # 如果 year 为 None，跳过该行
            if year is None:
                print(f"Skipping row due to invalid year: {row}")
                continue
            house_info = HouseInfo(
                house_info_link=house_info_link,
                house_address=house_address,
                house_type=house_type,
                house_area=float(house_area),
                orientation=orientation,
                decoration=decoration,
                floor=floor,
                year=year,
                house_category=house_category,
                price=float(price),
                city=city
            )
            db.session.add(house_info)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        reset_auto_increment()  # 重置自增 ID
        import_csv_to_mysql('杭州.csv')
        print("导入完成")
    app.run(debug=True)