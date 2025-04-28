import logging
import random

from sqlmodel import select, Session

from app.db import create_db_and_tables, engine
from app.db.models import (
    Bank, BankAccount,
    InsurancePolicyProduct, InsurancePolicyProductType,
    InvestmentProduct, InvestmentProductType,
    LoanProduct, LoanProductType,
    Transaction, TransactionType,
    User, UserProfile)
from app.utils.secrets import get_password_hash

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
_log = logging.getLogger(__name__)


def get_session_sync():
    return Session(engine)


def bootstrap_banks():
    with get_session_sync() as session:
        if session.exec(select(Bank)).all():
            _log.debug('[-] Skipping banks bootstrap...')
            return

        _log.debug('[i] Starting banks bootstrap...')

        banks = [
            Bank(name="Multiversity Bank", address="Via Roma, 1", phone="+390812345678"),
            Bank(name="UniPegaso Bank", address="Via Roma, 2", phone="+390812345678"),
            Bank(name="UniCredit", address="Via Roma, 3", phone="+390812345678"),
            Bank(name="Intesa SanPaolo", address="Via Roma, 4", phone="+390812345678"),
            Bank(name="Fineco Bank", address="Via Roma, 5", phone="+390812345678"),
            Bank(name="Banca BPM", address="Via Roma, 6", phone="+390812345678"),
            Bank(name="Banca Mediolanum", address="Via Roma, 7", phone="+390812345678"),
            Bank(name="BPER Banca", address="Via Roma, 8", phone="+390812345678"),
            Bank(name="Monte dei Paschi di Siena", address="Via Roma, 9", phone="+390812345678"),
            Bank(name="Illimity Bank", address="Via Roma, 10", phone="+390812345678")
        ]

        session.add_all(banks)
        session.commit()
        _log.debug('[+] Banks bootstrap done!')


def bootstrap_users_and_profiles():
    with get_session_sync() as session:
        if session.exec(select(User)).all():
            _log.debug('[-] Skipping users bootstrap...')
            return

        _log.debug('[i] Starting users bootstrap...')

        users = [
            User(
                name="Charles", surname="Leclerc",
                tax_identification_number="LCLCRL97R16Z123N",
                birth_date="1997-10-16", birth_country="MCO",
                birth_state="EE", birth_city="Monte Carlo"
            ),
            User(
                name="Lewis", surname="Hamilton",
                tax_identification_number="HMLLWS85A07Z114F",
                birth_date="1985-01-07", birth_country="GBR",
                birth_state="EE", birth_city="Stevenage"
            ),
            User(
                name="George", surname="Russell",
                tax_identification_number="RSSGRG98B15Z114G",
                birth_date="1998-02-15", birth_country="GBR",
                birth_state="EE", birth_city="King's Lynn"
            ),
            User(
                name="Andrea Kimi", surname="Antonelli",
                tax_identification_number="NTNNRK06M25A944I",
                birth_date="2006-08-25", birth_country="ITA",
                birth_state="BO", birth_city="Bologna"
            ),
            User(
                name="Max", surname="Verstappen",
                tax_identification_number="VRSMML97P30Z103R",
                birth_date="1997-09-30", birth_country="BEL",
                birth_state="EE", birth_city="Hasselt"
            ),
            User(
                name="Yuki", surname="Tsunoda",
                tax_identification_number="TSNYKU00E11Z219F",
                birth_date="2000-05-11", birth_country="JPN",
                birth_state="EE", birth_city="Sagamihara"
            ),
            User(
                name="Oliver", surname="Bearman",
                tax_identification_number="BRMLVR05E08Z114M",
                birth_date="2005-05-08", birth_country="GBR",
                birth_state="EE", birth_city="Chelmsford"
            ),
            User(
                name="Fernando", surname="Alonso",
                tax_identification_number="LNSFNN81L29Z131M",
                birth_date="1981-07-29", birth_country="ESP",
                birth_state="EE", birth_city="Oviedo"
            ),
            User(
                name="Lando", surname="Norris",
                tax_identification_number="NRRLND99S13Z114I",
                birth_date="1999-11-13", birth_country="GBR",
                birth_state="EE", birth_city="Bristol"
            ),
            User(
                name="Oscar", surname="Piastri",
                tax_identification_number="PSTSCR01D06Z700M",
                birth_date="2001-04-06", birth_country="AUS",
                birth_state="EE", birth_city="Melbourne"
            ),
            User(
                name="Nico", surname="Hülkenberg",
                tax_identification_number="HLKNCI87M19Z111S",
                birth_date="1987-08-19", birth_country="DEU",
                birth_state="EE", birth_city="Emmerich am Rhein"
            ),
            User(
                name="Gabriel", surname="Bortoleto",
                tax_identification_number="BRTGRL04R14Z602U",
                birth_date="2004-10-14", birth_country="BRA",
                birth_state="EE", birth_city="São Paulo"
            ),
            User(
                name="Liam", surname="Lawson",
                tax_identification_number="LWSLMI02B11Z719N",
                birth_date="2002-02-11", birth_country="NZL",
                birth_state="EE", birth_city="Hastings"
            ),
            User(
                name="Isack", surname="Hadjar",
                tax_identification_number="HDJSCK04P28Z110A",
                birth_date="2004-09-28", birth_country="FRA",
                birth_state="EE", birth_city="Paris"
            ),
            User(
                name="Pierre", surname="Gasly",
                tax_identification_number="GSLPRR96B07Z110S",
                birth_date="1996-02-07", birth_country="FRA",
                birth_state="EE", birth_city="Rouen"
            ),
            User(
                name="Jack", surname="Doohan",
                tax_identification_number="DHNJCK03A20Z700F",
                birth_date="2003-01-20", birth_country="AUS",
                birth_state="EE", birth_city="Gold Coast"
            ),
            User(
                name="Esteban", surname="Ocon",
                tax_identification_number="CNOSBN96P17Z110F",
                birth_date="1996-09-17", birth_country="FRA",
                birth_state="EE", birth_city="Évreux"
            ),
            User(
                name="Lance", surname="Stroll",
                tax_identification_number="STRLNC98R29Z401K",
                birth_date="1998-10-29", birth_country="CAN",
                birth_state="EE", birth_city="Montreal"
            ),
            User(
                name="Carlos", surname="Sainz",
                tax_identification_number="SNZCLS94P01Z131Y",
                birth_date="1994-09-01", birth_country="ESP",
                birth_state="EE", birth_city="Madrid"
            ),
            User(
                name="Alexander", surname="Albon",
                tax_identification_number="LBNLND96C23Z114F",
                birth_date="1996-03-23", birth_country="GBR",
                birth_state="EE", birth_city="London"
            )
        ]

        session.add_all(users)

        for user in users:
            user_email = '{}.{}@mail.com'.format(
                user.name[0].lower(), user.surname.lower()
            ).replace(" ", "")
            user_profile = UserProfile(
                email=user_email, password=get_password_hash("password"),
                user_id=user.id)
            session.add(user_profile)

        session.commit()
        _log.debug('[+] Users bootstrap done!')


def bootstrap_insurance_policy_products():
    with get_session_sync() as session:
        if session.exec(select(InsurancePolicyProduct)).all():
            _log.debug('[-] Skipping insurance_policy_products bootstrap...')
            return

        _log.debug('[i] Starting insurance_policy_products bootstrap...')

        insurance_policy_products = [
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.CAR,
                name="Assicurazione auto benzina",
                annual_premium=900,
                coverage_cap=1000000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.CAR,
                name="Assicurazione auto diesel",
                annual_premium=1000,
                coverage_cap=1000000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.CAR,
                name="Assicurazione auto ibrida",
                annual_premium=800,
                coverage_cap=1050000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.CAR,
                name="Assicurazione auto elettrica",
                annual_premium=700,
                coverage_cap=1100000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.LIFE,
                name="Assicurazione vita standard",
                annual_premium=850,
                coverage_cap=500000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.LIFE,
                name="Assicurazione vita premium",
                annual_premium=1500,
                coverage_cap=1000000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.LIFE,
                name="Assicurazione vita famiglia",
                annual_premium=2000,
                coverage_cap=2500000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.HOME,
                name="Assicurazione casa standard",
                annual_premium=700,
                coverage_cap=300000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.HOME,
                name="Assicurazione casa premium",
                annual_premium=1200,
                coverage_cap=750000
            ),
            InsurancePolicyProduct(
                type=InsurancePolicyProductType.HOME,
                name="Assicurazione casa platinum",
                annual_premium=2000,
                coverage_cap=1000000
            ),
        ]

        session.add_all(insurance_policy_products)
        session.commit()
        _log.debug('[+] insurance_policy_products bootstrap done!')


def bootstrap_investment_products():
    with get_session_sync() as session:
        if session.exec(select(InvestmentProduct)).all():
            _log.debug('[-] Skipping investment_products bootstrap...')
            return

        _log.debug('[i] Starting investment_products bootstrap...')

        investment_products = [
            InvestmentProduct(
                type=InvestmentProductType.CRYPTO,
                name="Bitcoin",
                rate=6.5
            ),
            InvestmentProduct(
                type=InvestmentProductType.ETF,
                name="Vanguard=P 500 ETF",
                rate=8.2
            ),
            InvestmentProduct(
                type=InvestmentProductType.FUND,
                name="Pict=Water Fund",
                rate=4.3
            ),
            InvestmentProduct(
                type=InvestmentProductType.ACTION,
                name="Apple Inc.",
                rate=9.1
            ),
            InvestmentProduct(
                type=InvestmentProductType.BOND,
                name="Treasury 10Y",
                rate=3.5
            ),
            InvestmentProduct(
                type=InvestmentProductType.RAW_MATERIALS,
                name="Gold",
                rate=2.7
            ),
            InvestmentProduct(
                type=InvestmentProductType.CRYPTO,
                name="Ethereum",
                rate=7.8
            ),
            InvestmentProduct(
                type=InvestmentProductType.FUND,
                name="BlackRock Global Allocation",
                rate=5.0
            ),
            InvestmentProduct(
                type=InvestmentProductType.ACTION,
                name="Tesla Inc.",
                rate=11.4
            ),
            InvestmentProduct(
                type=InvestmentProductType.ETF,
                name="iShares MSCI Emerging Markets",
                rate=6.1
            )
        ]

        session.add_all(investment_products)
        session.commit()
        _log.debug('[+] investment_products bootstrap done!')


def bootstrap_loan_products():
    with get_session_sync() as session:
        if session.exec(select(LoanProduct)).all():
            _log.debug('[-] Skipping loan_products bootstrap...')
            return

        _log.debug('[i] Starting loan_products bootstrap...')

        loan_products = [
            LoanProduct(
                type=LoanProductType.PERSONAL_LOAN,
                name="Prestito Facile",
                rate=5.9
            ),
            LoanProduct(
                type=LoanProductType.HOME_MORTGAGE,
                name="Mutuo Tasso Fisso 20 anni",
                rate=2.3
            ),
            LoanProduct(
                type=LoanProductType.CREDIT_CARD,
                name="Carta di Credito Classic",
                rate=16.5
            ),
            LoanProduct(
                type=LoanProductType.PERSONAL_LOAN,
                name="Prestito Online",
                rate=6.2
            ),
            LoanProduct(
                type=LoanProductType.HOME_MORTGAGE,
                name="Mutuo Giovani 20 anni",
                rate=2.0
            ),
            LoanProduct(
                type=LoanProductType.CREDIT_CARD,
                name="Carta Revolving",
                rate=17.8
            ),
            LoanProduct(
                type=LoanProductType.PERSONAL_LOAN,
                name="Prestito Flessibile",
                rate=5.5
            ),
            LoanProduct(
                type=LoanProductType.HOME_MORTGAGE,
                name="Mutuo Variabile 30 anni",
                rate=1.9
            ),
            LoanProduct(
                type=LoanProductType.CREDIT_CARD,
                name="Carta Oro",
                rate=15.9
            ),
            LoanProduct(
                type=LoanProductType.PERSONAL_LOAN,
                name="Prestito Personale",
                rate=6.8
            )
        ]

        session.add_all(loan_products)
        session.commit()
        _log.debug('[+] loan_products bootstrap done!')


def bootstrap_bank_accounts():
    with get_session_sync() as session:
        if session.exec(select(BankAccount)).all():
            _log.debug('[-] Skipping bank_accounts bootstrap...')
            return

        _log.debug('[i] Starting bank_accounts bootstrap...')

        banks = session.exec(select(Bank)).all()
        user_profiles = session.exec(select(UserProfile)).all()

        bank_accounts = []
        for user_profile in user_profiles:
            index = random.randint(0, len(banks) - 1)
            bank = banks[index]
            bank_accounts.append(
                BankAccount(
                    bank_id=bank.id,
                    currency="EUR",
                    user_profile_id=user_profile.id,
                    balance=5000
                )
            )
        session.add_all(bank_accounts)
        session.commit()
        _log.debug('[+] bank_accounts bootstrap done!')


def bootstrap_transactions():
    def _add_transaction(session, transaction_type, *bank_account_ids):
        amount = random.uniform(1, 200)
        transaction = Transaction(
            amount=round(amount, 2),
            fee=random.randint(0, 5),
            type=transaction_type
        )

        if transaction_type is TransactionType.DEPOSIT:
            transaction.destination_account_id = bank_account_ids[0]
            transaction.description = "Deposito contanti"
        elif transaction_type is TransactionType.WITHDRAW:
            transaction.source_account_id = bank_account_ids[0]
            transaction.description = "Prelievo contanti"
        elif transaction_type is TransactionType.TRANSFER:
            transaction.source_account_id = bank_account_ids[0]
            transaction.destination_account_id = bank_account_ids[1]
            if amount <= 20:
                transaction.description = "Acquisto Libro"
            elif amount <= 100:
                transaction.description = "Acquisto Orologio"
            else:
                transaction.description = "Acquisto Notebook"
        session.add(transaction)

    with get_session_sync() as session:
        if session.exec(select(Transaction)).all():
            _log.debug('[-] Skipping transactions bootstrap...')
            return

        _log.debug('[i] Starting transactions bootstrap...')

        bank_accounts = session.exec(select(BankAccount)).all()

        for index, source_bank_account in enumerate(bank_accounts):
            destination_account_index = None
            while destination_account_index is None or destination_account_index == index:
                destination_account_index = random.randint(0, len(bank_accounts) - 1)
            destination_bank_account = bank_accounts[destination_account_index]
            _add_transaction(session, TransactionType.DEPOSIT, source_bank_account.id)
            _add_transaction(session, TransactionType.WITHDRAW, source_bank_account.id)
            _add_transaction(
                session, TransactionType.TRANSFER, source_bank_account.id,
                destination_bank_account.id)

        session.commit()
        _log.debug('[+] transactions bootstrap done!')


if __name__ == "__main__":
    create_db_and_tables()
    bootstrap_banks()
    bootstrap_insurance_policy_products()
    bootstrap_investment_products()
    bootstrap_loan_products()
    bootstrap_users_and_profiles()
    bootstrap_bank_accounts()
    bootstrap_transactions()
