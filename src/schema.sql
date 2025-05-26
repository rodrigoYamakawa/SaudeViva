
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL -- WARNING: Storing plain text passwords!
        );

        CREATE TABLE IF NOT EXISTS glucose_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level INTEGER NOT NULL,
            timestamp TEXT NOT NULL, -- Storing as TEXT from datetime-local input
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        