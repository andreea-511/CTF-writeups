The hint for this challenge is 
```
Dear Agent, as your first task within the Agency, find the last known location of tecgirwilliam@gmail.com also called Tecgir William without attempting to hack or bruteforce within any account. All information is of course public. After that maybe we can have that call over Google Hangouts/Meets (or both) about how to clean the cafeteria.

Note: The flag of this code must be generated as such: CTF{sha256sum('Google Plus Code')}
```
Since we are provided an e-mail and we need to find a Google Plus Code let's try using [tools.epieos.com](https://tools.epieos.com/email.php) with the provided email.
\
We get the following information:
```
Email : tecgirwilliam@gmail.com

Name : Tecgir William

GoogleID : 111076247952673225160

Last Update : 2021-12-02 09:42:10

Hangouts

Maps https://www.google.com/maps/contrib/111076247952673225160

Calendar : https://calendar.google.com/calendar/htmlembed?src=tecgirwilliam@gmail.com
```
If we check the Google Maps link we can see that we find the profile of Tecgir William as a Local Guide and clicking on `Cascada Lotrișor` and checking the reviews we notice that our wanted man has reviewed this places as 5 stars.
\
All that is left to do is copy the Google Plus Code of the location which is `872J+WX Brezoi` and convert it to sha256
```
echo -n "872J+WX Brezoi" | sha256sum
```
which results in
```
e0c34f6ffe1dcc87c67a4fa218b1050da7bb9b9d01871ea7afcb49e55b81257d
```
thus our flag is
```
CTF{e0c34f6ffe1dcc87c67a4fa218b1050da7bb9b9d01871ea7afcb49e55b81257d}
```
