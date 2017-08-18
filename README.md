ffmpeg-lambda
===
Run ffmpeg inside a lambda for serverless transformations.

## Static Binaries
Grab the `x86_64 build` files from [ffmpeg static builds](https://www.johnvansickle.com/ffmpeg/).

Put `ffmpeg` static binary into into the `bin` subdirectory and delete everything else.

## Dev
```bash
pip install zappa flask
# export AWS secret/key/region etc
zappa init
zappa deploy dev
# make changes as needed
zappa update dev
# watch logs
zappa tail dev
```

## Production
Keep in mind limitations of lambda e.g. max runtime, CPU, and RAM etc.
You may need/want to add the following to your `zappa_settings.json`
```
"binary_support": true,
"cors": true,
```

## Todo
- [ ] production deploy
- [ ] ssl
- [x] streaming response
- [ ] better logging based on debug level
- [ ] standardize on JSON response for all errors/version endpoints etc

## Implications
You can stick almost any smallish `x86_64` statically compiled binary
e.g. `golang` etc into `bin` and call it via http! Cheers!

## Notes
I haven't implemented actual useful transformations in this
version. Sorry. Just pass arguments and keep in mind that ffmpeg
can read in http streams directly or use `stdin` and `stdout`.

## References
* [Miserlou/Zappa](https://github.com/Miserlou/Zappa)
* [ubergarm/pythumbio](https://github.com/ubergarm/pythumbio)
