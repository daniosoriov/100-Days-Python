signature = f"""\
<br /><br />
            Dani
            <br /><br />
            <small><em>This email was automatically created using ChatGPT via a script I created.
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

html_openai = f"""\
<html>
    <body>
        <div>
            [OPENAI_TEXT]
            {signature}
        </div>
    </body>
</html>
"""

