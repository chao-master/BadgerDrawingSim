## What?
A rough attempt to make a badger2040 "simulator", by which I mean something that roughly simulates the drawing methods of the badger2040

## Why?
At this point, mostly to see if I can do it

## How?
`bridge` contains custom written implemnetations of key modules that the badger2040 requires to run, but done in such a way that result in us being able to see the result on the PC, noteably the `badger2040` module, that implements the drawing methods to draw to a `tkinter` window.

`micropython` contains modules and libaries taken right from the [pimoroni github](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython) (Which is MIT licensed), which is also the source of the examples `badge.py` and `fonts.py`. These files are all unmodified, except minor changes to prevent them trying to read files from the root directory, and instead point them into `badger-system`. I ideally need a better way to chroot them.

It's worth noting that this isn't the best way to do this, and there are several issues, some of which I may be able to solve

1. This is not an emulator, it will not replicate the metal of the microprocessor
2. I couldn't be bothered to implement the dithering algorith, so the output just has the 16 shades of grey.
3. There are no interrupts
4. Button handling only happens inside `Badge2040.halt()`, as this is the only time the tkinter update loop runs.
5. The system only attempts to simulate the badger as it runs on USB power, so a lot of commands are just stright up ignored
6. The whole of `machine.py` is missing, it's only there because `badger_os.py` wants it, but the parts of `badger_os` used by the demos, don't use `machine`.
7. Bitmap fonts are not supported