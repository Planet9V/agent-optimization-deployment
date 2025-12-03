
https://www.youtube.com/watch?v=o_AdotbIbvk

## ntro

My name is Jesse.

My name is Sever. In this video,

you’ll see our latest cybersecurity solution for power substations.

Now, before we begin,

let’s cover some basics.

The poster behind me

is a simplified diagram of the power grid.

## Power Grid

The electricity we all use is generated

from the power plants on the left hand side,

then delivered to consumers

through the transmission and distribution networks.

The whole grid is made of substations and power lines.

The major parts where cybersecurity is applied

is substation automation systems.

Here we have a more vivid model to represent

the power grid of a city.

It includes the power plant,

the high voltage substation,

the low voltage substation,

and the industrial and residential consumers.

As an industrial networking solution provider for power automation,

we care about cybersecurity.

So next, we want to show you

one of the possible attack scenarios to substations

and what are the countermeasures that we could do

to prevent it from happening.

## Intelligent Electronic Device

This is a simplified substation network architecture.

The key component here is

IIntelligent Electronic Device (IED).

Its job is to protect the primary equipment

and power grid from damage caused by

voltage, current, or frequency anomalies.

Modern IEDs are connected via

Ethernet networks to each other

as well as to the SCADA system,

which is a human machine interface

for operators to control the entire facility.

So these two components: IED and SCADA

are the most critical

and could be the primary cyber-attack targets.

The attack vectors may include compromised WAN links

as well as internal attacks

through removable medias

or other unauthorized devices.

## Test Bed

Let’s see what may happen

if adversaries get access to the substation network.

We have built a test bed

consist of two IEDs,

a SCADA server,

which are connected through Ethernet switch.

Also we have an additional cybersecurity appliance here

which we will introduce later.

## Trick ID

The first example is to trick the IED

to trigger its protection.

Let me use my attack tool and target IED.

As you can see, the residents of this city

are going to have a romantic evening with candles.

## Scada

The target for the second example is SCADA.

What I can do here

is to disrupt its operation.

This will leave the substation personnel without control,

making it much harder to handle the incident.

I think you all agree that

these examples showed serious impact,

so let’s take a deep dive into

what exactly happened,

and how we can prevent it from happening.

In the first scenario,

## Boos

I exploited the IED to IED communication protocol

which is called GOOSE.

It is used for one IED

to report its status to another IED,

so protection functionality can span

across different areas of the substation.

If there is a failure in one bay,

the other bay's protection should react accordingly.

GOOSE was originally designed unencrypted

because of its time-critical nature.

There is an additional standard

which implies digital signing of GOOSE messages,

however it's not widely adopted yet.

Also, for time critical reasons,

GOOSE uses multicast transmission,

so it's easy for an attacker to sniff messages,

study its contents,

and forge a malicious packet

that mimics IED announcement about failure.

This is exactly what I did with my attack tool

during the demo.

It’s not practical to put firewalls between IEDs

because it will add unacceptable latencies.

So our solution is based on Ethernet switch.

MOXA PT Series provides a special feature

which is called, “GOOSE Check”.

It recognizes GOOSE protocols,

remembers legitimate flows, and detects tampering activities.

During the commissioning stage,

## Goose Check

we can verify that all GOOSE flows are legit

via the switch user interface.

Then we can lock it by enabling “GOOSE Lock”,

and tell the switch to drop abnormal GOOSE messages.

Now let me try to run the same attack again.

As you can see, nothing happens.

And our happy residents can keep watching TV.

This is because the switch successfully detected the tampering attack

and dropped malicious packets.

Although the attacker created identical packets

to the packets that the IED would send

in case of a failure,

the switch knows that they are coming from

a different physical port,

which triggers tampering detection

and filters the malicious messages out.

Such filtering is performed on a hardware level,

so it doesn’t add any latency.

By the way, the GOOSE Check feature can also

be used for troubleshooting

because it provides some information about the flows.

During the second attack,

## Second Attack

I exploited a known vulnerability of

SCADA computer’s operating system.

Actually SCADAs usually run on top of Windows,

in other words, they are similar to our home and office computers.

The difference is, however,

that they are not patched regularly.

This is because any change in critical automation systems

has to be verified and approved.

So you can find many outdated software in the field.

In this example,

we have an unpatched Windows 7 computer,

so I was able to use a publicly available exploit for RDP protocol

and easily cause the whole system to halt.

To overcome these challenges,

## Virtual Patch

we can put an additional protection like IPS

in front of SCADA computers.

It can provide a function called “Virtual Patch”.

The majority of vulnerabilities

are executed through the network.

So if we deploy IPS empowered with threat intelligence

about known vulnerabilities,

we can prevent the exploitation

by dropping traffic related to the attack.

In other words, we may delay patching of vulnerable systems

by applying a “virtual patch” on the IPS.

## IPs

Having introduced the IPS,

let me show you how it works.

This is the web user interface

of EtherCatch IPS from MOXA.

By sliding the toggle

I am enabling pattern-based protection against OT&IT attacks.

By the way, the patterns are updated regularly

to keep up with the latest security advisories.

Now that the protection is on,

let’s try to execute the same attack one more time.

As you can predict,

the SCADA remains fully functional

because the attack was blocked.

## Conclusion

This can also be seen in the logs of the IPS unit.

In addition, EtherCatch provides you

OT protocol aware firewall functionality

to further strengthen your network security.

MOXA provides a wide range portfolio

of IEC 61850 compliant products for power automation.

In the brief demonstration,

we showed you some security features of MOXA solutions.

For more details,

please visit our website at

www.moxa.com/security

or contact our partner in your region.

Thanks for watching, and see you next time.

www.moxa.com/security

or contact our partner in your region.

Thanks for watching, and see you next time.

English (United States)

AllFrom MoxaComputer securityInformation technologyComputer HardwareComputer Science