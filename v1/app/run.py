import v1.app.entities as entities

runtime_environment = "development"

def main():
    a = entities.Example()
    oracle_run = a.run_oracle_query()
    email_run = a.run_send_email()

if __name__ == '__main__':
    main()