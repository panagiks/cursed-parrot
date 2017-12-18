# cursed-parrot
Speak in tongues now - give them the dictionary later

## Project Status

Δ! Early PoC. Nothing functional just thoughts spewed in code form.
Stay tunned though ;) !Δ

## What it does.

Select recipients, write a message and have an encrypted version of it sent to
them. Select a time in the future and we'll mail them the decryption key.

Want a dead man's switch? We've got you covered! Just log in before the time
your message is due to be send and reschedule it.

## Security Considerations

This is not an OTR communication or in any way more secure or secret(ive) than
traditional email. Both the encrypted message and the decryption key will be
sent to the recipients via email. Anyone in a position to capture an email will
also be able to capture both the parts needed to reconstruct it (encrypted
message and decryption key). Think of it as a delayed delivery mail with the
ability to prove when you send the message, since the recipient has the message
from the first moment but just can't read it.
