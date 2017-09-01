# everest3

Hi team, 

Let's get the ball rolling on _everest3_ this fall. I added all of you to the repo as you've expressed interested in contributing to _everest_ at some point in the past. If you want no part in this, let me know and I'll get you off the list.

Here are my thoughts for the new version:

- **A complete re-write of the code** The current code is quite clunky and not that developer-friendly
- **Speed up the GP with celerite** We will simultaneously optimize the GP and the PLD parameters since _celerite_ is so fast. This will be awesome for stellar rotation studies
- **Code should be mission-independent** I tried to do this with _everest2_ but didn't really succeed. It should work for _Kepler_ (and ideally TESS) out-of-the-box
- **Code should be less exoplanet-specific** Lots of people interested in supernovae/asteroseismology/etc would like to use **everest**
- **Fix overfitting issues** We need to investigate what's going on with _nPLD_, particularly during thruster fires
- **Code with Campaigns 16+ in mind** The roll will get really bad once the thrusters start sputtering. NKS and I are currently working on this
- **Re-think PLD** PLD is great but somewhat hacky. Normalizing the pixels by the SAP flux introduces more noise into the regressors and is un-Bayesian. There may be a more elegant (and efficient) way to de-trend

I'm currently running Campaigns 10-13 with the old code. Hopefully these will be the last ones we'll tackle with version 2, and we can start fresh with _everest3_ when Campaign 14 comes out at the end of the year.

I'll put together some skeleton code in the next few weeks and try to assign jobs to people. Stay tuned.

Rodrigo
