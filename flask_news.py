"""
Created by newming at 2018/10/2
"""

from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import NewsForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:woaiwojia.@localhost:3306/net_news?charset=utf8'
app.config['SECRET_KEY'] = 'newming'
db = SQLAlchemy(app)


class News(db.Model):
	# 表名称
	__tablename__ = 'news'
	# 各个字段
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	content = db.Column(db.String(2000), nullable=False)
	types = db.Column(db.String(10), nullable=False)
	image = db.Column(db.String(300), )
	author = db.Column(db.String(20), )
	view_count = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=1)

	def __repr__(self):
		return '<News %r>' % self.title


# new_obj = News(
# 	title='标题1',
# 	content='内容',
# 	types='百家'
# )

# 创建表
# db.create_all()

# 插入数据
# db.session.add(new_obj)
# db.session.commit()

# 打印的结果格式是由上边 __repr__ 函数决定的，没有的话打印的就是内存地址
# print(News.query.all())


@app.route('/')
def index():
	# 新闻首页
	news_list = News.query.filter_by(is_valid=True)
	return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>')
def cat(name):
	# 新闻类别
	news_list = News.query.filter(News.types == name).filter(News.is_valid == True)
	return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<int:pk>')
def detail(pk):
	# 新闻详情信息
	new_obj = News.query.get(pk)
	return render_template('detail.html', pk=pk, new_obj=new_obj)


@app.route('/admin')
@app.route('/admin/<int:page>')
def admin(page = None):
	# http://flask-sqlalchemy.pocoo.org/2.3/api/#flask_sqlalchemy.BaseQuery.paginate 分页
	# 后台首页
	if page is None:
		page = 1
	news_list = News.query.paginate(page=page, per_page=5)
	# print(news_list.items)
	return render_template('admin/index.html', news_list=news_list)


@app.route('/admin/update/<int:pk>', methods=('GET', 'POST'))
def update(pk):
	# 更新
	new_obj = News.query.get(pk)
	if not new_obj:
		return redirect(url_for('admin'))
	# 将表单默认显示的值传入
	form = NewsForm(obj=new_obj)
	if form.validate_on_submit():
		# 获取数据 -> 保存数据
		new_obj.title = form.title.data
		new_obj.content = form.content.data
		new_obj.types = form.types.data
		new_obj.image = form.image.data
		new_obj.created_at = datetime.now()

		db.session.add(new_obj)
		db.session.commit()
		return redirect(url_for('admin'))

	return render_template('admin/update.html', form=form, pk=pk)


@app.route('/admin/add', methods=('GET', 'POST'))
def add():
	# 新增
	form = NewsForm()
	if form.validate_on_submit():
		# 获取数据 -> 保存数据
		new_obj = News(
			title=form.title.data,
			content=form.content.data,
			types=form.types.data,
			image=form.image.data,
			created_at=datetime.now()
		)
		db.session.add(new_obj)
		db.session.commit()
		return redirect(url_for('admin'))
	return render_template('admin/add.html', form=form)


@app.route('/admin/delete/<int:pk>', methods=('GET', 'POST'))
def delete(pk):
	new_obj = News.query.get(pk)
	if not new_obj:
		return 'no'
	# 物理删除
	# db.session.delete(new_obj)
	new_obj.is_valid = False
	db.session.add(new_obj)
	db.session.commit()
	return 'yes'


if __name__ == '__main__':
	app.run(debug=True)
