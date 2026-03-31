import subprocess
import datetime
import os

def backup_mysql_db(host, user, password, db_name, backup_dir):
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Format filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

    # Construct mysqldump command
    command = [
        "mysqldump",
        f"-h{host}",
        f"-u{user}",
        f"-p{password}",
        db_name
    ]

    # Run the command and write to file
    with open(backup_file, "w") as f:
        subprocess.run(command, stdout=f)

    print(f"MySQL backup completed: {backup_file}")


timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
backup_dir=os.path.join(f"C:\mysql_database",timestamp)


backup_mysql_db(
    host="localhost",
    user="root",
    password="Paresh@123",
    db_name="trade_india_company_data",
    backup_dir=backup_dir
)
