from flask import Flask, render_template
import mysql.connector
import time
import sys

app = Flask(__name__)

# Try to connect to MySQL with multiple retries
max_retries = 20
db = None

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt + 1}/{max_retries}: Connecting to MySQL...")
        db = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="testdb"
        )
        if db.is_connected():
            print("✅ Successfully connected to MySQL!")
            break
    except Exception as e:
        print(f"⚠️ Connection failed: {e}")
        time.sleep(5)

if db is None or not db.is_connected():
    print("❌ Could not connect to MySQL after all retries")
    # Create a fallback - app will work without MySQL for testing
    db = None

@app.route('/')
def home():
    count = 0
    try:
        if db and db.is_connected():
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS visitors (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            cursor.execute("INSERT INTO visitors (name) VALUES ('Visitor')")
            db.commit()
            cursor.execute("SELECT COUNT(*) FROM visitors")
            count = cursor.fetchone()[0]
            print(f"✅ Visitor count: {count}")
        else:
            # Fallback: increment in memory if DB not available
            global memory_count
            if 'memory_count' not in globals():
                memory_count = 0
            memory_count += 1
            count = memory_count
            print(f"⚠️ Using in-memory count: {count}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        count = "Error"

    return render_template("index.html", count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
