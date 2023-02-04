import pandas

df = pandas.read_csv('hotels.csv', dtype={'id': str})
df_cards = pandas.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_cards_security = pandas.read_csv('card_security.csv', dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        '''Book a hotel by changing availability to no'''
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        '''Check if the hotel is available'''

        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f'''
        Thank you for your reservation!
        Here are your booking data
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
'''
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        cardData = {'number': self.number, 'expiration': expiration, 'holder': holder, 'cvc': cvc}

        if cardData in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


class Spa(Hotel):
    def bookSpaHotel(self):
        pass


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate1(self):
        content1 = f'''
        Thank you for your SPA reservation!
        Here are your booking data
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
'''
        return content1


print(df)

hotel_ID = input('Enter the id of the hotel : ')
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number='1234567890123456')
    if credit_card.validate(expiration='12/26', cvc='325', holder='Jason Statham'):
        if credit_card.authenticate(given_password='mypass'):

            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())

            spa = input('Do you want the spa package?')
            if spa == 'yes':
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate1())
        else:
            print('Credit Card authentication failed.')
    else:
        print("There was a problem with your payment")
