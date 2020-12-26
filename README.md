We live busy lives these days. Between work, chores, and other things in our to-do lists, it can be tough to catch your breath and stay calm. Credit cards are one of the things that save us time, energy, and nerves. From not having to carry a wallet full of cash to consumer protection, cards make our lives easier in many ways. In this project, I developed a simple banking system with a database.

If you’re curious about business, technology, or how things around you work, you'll probably enjoy learning how credit card numbers work. These numbers ensure easy payments, and they also help prevent payment errors and fraud. Card numbers are evolving, and they might look different in the near future.

Let's take a look at the anatomy of a credit card:
![alt text](https://github.com/Ilyassov/Simple-Banking-System/blob/main/card.png?raw=true)

The very first number is the Major Industry Identifier (MII), which tells you what sort of institution issued the card.

    1 and 2 are issued by airlines
    3 is issued by travel and entertainment
    4 and 5 are issued by banking and financial institutions
    6 is issued by merchandising and banking
    7 is issued by petroleum companies
    8 is issued by telecommunications companies
    9 is issued by national assignment

In my banking system, credit cards begin with 4.

The first six digits are the Issuer Identification Number (IIN). These can be used to look up where the card originated from. If you have access to a list that provides detail on who owns each IIN, you can see who issued the card just by reading the card number.

Here are a few you might recognize:

    Visa: 4*****
    American Express (AMEX): 34**** or 37****
    Mastercard: 51**** to 55****

In my banking system, the IIN is 400000.

The seventh digit to the second-to-last digit is the customer account number. Most companies use just 9 digits for the account numbers, but it’s possible to use up to 12. This means that using the current algorithm for credit cards, the world can issue about a trillion cards before it has to change the system.

We often see 16-digit credit card numbers today, but it’s possible to issue a card with up to 19 digits using the current system. In the future, we may see longer numbers becoming more common.

In my banking system, the customer account number can be any, but it should be unique. And the whole card number is 16-digit length.

The very last digit of a credit card is the **check digit** or **checksum**. It is used to validate the credit card number using the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm).