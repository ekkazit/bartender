การติดตั้ง
---------


1. ติดตั้ง PostgreSQL หรือ MySQL (แนะนำ PostgreSQL 9.3+)
	password: password


2. ตั้งค่า PATH ใน environment variable ชี้ไปยัง bin ของ PostgreSQL เช่น PATH=C:\Program Files\PostgreSQL\9.4\bin


3. สร้าง PostgreSQL database ชื่อว่า pospax
* หมายเหตุ: ชื่อ pospax


4. ติดตั้ง Tomcat ให้เรียบร้อย


5. ก็อปปี้ postgresql-9.4-1202.jdbc4.jar จาก bartender/birt ไปใส่ใน <TOMCAT_HOME>\lib


6. ก็อปปี้โฟลเดอร์ birt.zip จาก bartender/birt ไปใส่แล้ว unzip ไว้ใน <TOMCAT_HOME>\webapps

สั่ง run tomcat แล้วทดสอบ http://localhost:8080/birt
หรือ
http://localhost:8080/birt/frameset?__report=bill.rptdesign

-------------

7. ติดตั้ง libs ที่ใช้ใน bartender ด้วยคำสั่งดังนี้

$  mkdir c:\startup
$  cd c:\startup
$  virtualenv envs

$  cd c:\startup\envs
$  Script\activate

*ถ้าเป็น Ubuntu จะใช้ source bin\activate

$  pip install -r requirements.txt



8. ดึง source code ออกมาจาก github

(envs)$  mkdir c:\startup\envs\bartender
(envs)$  git init
(envs)$  git remote add origin https://github.com/ekkazit/bartender.git
(envs)$  git pull origin master


9. สร้างเทเบิ้ลด้วยคำสั่ง

(envs)$  python manage.py migrate



10. สร้างข้อมูลจำลองด้วยคำสั่ง

(envs)$  python manage.py seed



11. จากนั้นสั่งให้โปรแกรมเว็บทำงาน

(envs)$  python manage.py runserver



12. เข้าใช้งานด้วยยูอาร์แอล http://localhost:5000/pos หรือ http://localhost:5000/home
