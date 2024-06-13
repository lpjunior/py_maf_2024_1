from database import create_connection, create_table, insert_user, select_all_users, update_user, delete_user


def main():
    database = r"users.db"
    conn = create_connection(database)

    if conn is not None:
        create_table(conn)

        # Insert users
        user_1 = ('Alice', 30)
        user_2 = ('Bob', 25)
        insert_user(conn, user_1)
        insert_user(conn, user_2)

        # Query and display all users
        print("Users before update:")
        select_all_users(conn)

        # Update user
        update_user(conn, ('Alice', 35, 3))  # Update user with id 1 to age 35

        # Query and display all users
        print("\nUsers after update:")
        select_all_users(conn)

        # Delete user
        delete_user(conn, 2)  # Delete user with id 2

        # Query and display all users
        print("\nUsers after delete:")
        select_all_users(conn)
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()
