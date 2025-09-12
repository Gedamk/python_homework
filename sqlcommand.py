import sqlite3

def main():
    # connect to lesson.db
    conn = sqlite3.connect("db/lesson.db")
    cur = conn.cursor()

    print("Connected to lesson.db. Type SQL commands or 'quit' to exit.")

    while True:
        try:
            cmd = input("sql> ")
            if cmd.strip().lower() in ["quit", "exit"]:
                break
            if not cmd.strip():
                continue

            cur.execute(cmd)
            results = cur.fetchall()

            # Print results in rows
            for row in results:
                print(row)

            conn.commit()

        except Exception as e:
            print("Error:", e)

    conn.close()

if __name__ == "__main__":
    main()
