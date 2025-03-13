SYSTEM_INSTRUCTION = """
You are a world-class birthday wisher, known for your warmth and creativity.

You are tasked with creating a personalized birthday wish for someone.

Follow these guidelines:
1. Pay attention to the name of the person.
2. Start with a cheerful greeting addressing the person by name.
3. Do not mention age.
4. Use '<br />' instead of new lines for propper formatting. It will be sent as HTML. Use double line breaks for paragraphs.
5. It should contain: [variables]. Feel free to use their name in a humorous way to connect the elements.
6. Smoothly connect these elements with humor and joy, ensuring the message flows naturally.
7. Conclude by reminding the person of the beauty of being alive.
8. Do not sign the letter or add any closing signature.
9. Strike a balance between being friendly and not overly personal, as some recipients may not be close friends.
10. Your messages are vegan, so, there is no mention of any animal product. Also, no animal cruelty or animal usage in any way.
"""

USER_MESSAGE = """Create a birthday wish for: [NAME]"""

variables = {
    'jokes': [
        'a dad joke',
        'a famous quote by a commedian about birthdays',
        'a word play/pun',
        'a joke about aging',
        'a joke about growing old',
        'a vegan joke',
        'a knock-knock joke',
        'a tech-related joke',
        'a light-hearted insult joke',
        'a joke about work',
    ],
    'facts': [
        'an incredibly overlooked fact',
        'a fact about the universe',
        'an age/aging fact',
        'a cute fact about a random animal',
        'a very exciting mathematical fact',
        'an impressive positive historical event',
        'a fun fact about a famous person',
        'a surprising fact about food',
        'a fact about a random country',
        'a fact about human body',
    ],
    'quotes': [
        'a love quote',
        'a friendship quote',
        'a movie quote',
        'a wisdom quote',
        'a stoic quote',
        'a quote from Incubus',
        'a motivational quote',
        'a quote from a famous author',
        'a quote from a historical figure',
        'a quote from a popular TV show',
    ]
}

signature = f"""\
<br /><br />
            Dani
            <br /><br />
            <small><em>This email was automatically created using an LLM (a.k.a AI) via a script I created.
            <br />I know the letter is a bit random but it comes with an intent I crafted.
            <br />You now have three choices:
            <br /><strong>Do nothing</strong>: you will get a similar email next year for your birthday :-)</li>
            <br /><strong>Go away</strong>: reply to this email saying "DELETE" and I will remove you from my 
            automated emails, or...
            <br /><strong>Reply</strong>: reply with a random message of your own to indulge me :-P</em></small>"""

html_ninja = f"""\
<html>
    <body>
        <div>
            Hi [NAME]! Happy birthday!
            <br /><br />
            I wanted to send you a birthday wish with a very random message. Let\'s jump in!
            <br /><br />
            Since I am a dad, here you have a <strong>dad joke</strong> to start:
            <br /><br />
            <em>[DAD_JOKE]</em>
            <br /><br />
            Ok, maybe that was not very good, how about a <strong>real joke</strong>?
            <br /><br />
            <em>[JOKE]</em>
            <br /><br />
            Maybe you didn't laugh, so in case you prefer something more serious, here's <strong>a fact</strong>:
            <br /><br />
            <em>[FACT]</em>
            <br /><br />
            Oops, too factual? How about a <strong>"love" quote</strong>?
            <br /><br />
            <em>[QUOTE]</em>
            <br /><br />
            Ultimately, what I really want is to send you a happy birthday! So, <strong>happy birthday!</strong>
            {signature}
        </div>
    </body>
</html>
"""

HTML_TEMPLATE = f"""\
<html>
    <body>
        <div>
            [LLM_TEXT]
            {signature}
        </div>
    </body>
</html>
"""
