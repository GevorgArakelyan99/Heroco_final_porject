import argparse
import database
import Autoorization as az


def main():
    login = False
    user = az.Check(0, 0, 0)

    parser = argparse.ArgumentParser(
        description='This program will help you find a film to watch from the 100 best movies based on https://stacker.com.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    parser_registration = subparsers.add_parser('registration', help='Register a new user')

    parser_login = subparsers.add_parser('login', help='Log in an existing user')

    parser_scrap = subparsers.add_parser('scrap',
                                         help='Scrape films top 100 from a https://stacker.com/movies/100-best-movies-all-time')

    parser_logout = subparsers.add_parser('logout', help='Logout from your account')

    args = parser.parse_args()

    if args.command == 'registration':
        check_username = user.username_check(0)
        checked_email = user.email_check(0)
        valid_pass = user.password_reg(0)
        if az.user_add(check_username, checked_email, valid_pass):
            print('Successfully registered')


    elif args.command == 'login':
        az.login(0, 0)



    elif args.command == 'scrap':
        if not az.is_logged_in():
            print('Please login first.')
        else:
            database.film_DB_adding(0)
            print('Data scraped successfully')

    elif args.command == 'logout':
        az.clear_login_status()
        print("Logged out successfully")


if __name__ == "__main__":
    main()
