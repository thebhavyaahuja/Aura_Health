## The Basics Computer Networking of

<!-- image -->

## What is a Computer Network?

## Interconnected Devices

- A network is simply a collection of connected devices that can share resources and data.
- Think of it like a road system connecting different cities.

The Internet is the biggest network of all-a global network of computers.

## Data Exchange

Networks allow the exchange of data, files, and information between the connected devices, enabling collaboration, resource sharing, and access to online services.

## Network Engineer

<!-- image -->

WhatmyfriendsthinkIdo.

<!-- image -->

What my boss thinks I do.

<!-- image -->

What my mom thinks I do

<!-- image -->

What I think I do.

What society thinks I do

<!-- image -->

WhatI actually do.

<!-- image -->

0

S

N

e

t

W

K

## Layers of a Network

## Application Layer

Presentation Layer

Session Layer

## Transport Layer

## Network Layer

## a Link Layer Data

Physical Layer

- N/w access to Application e.g. Web Browser (IE, Mozilla Firefox, Google Chrome)
- Type of Data; HTTPS - Encryption Sevices
- Starts and Ends session and also keeps them isolated.
- Defines Ports and Reliability
- Logicalor IP addressing; Determines Best path for the destination.
- Switches
- MAC Addressing
- Cable
- Network Interface Cards- Electric Signals

## The Role of the Transport Layer

Main Job: Provide logical communication between applications running on different hosts.

The Transport Layer (TCP/UDP):

- Responsibility: Process-to-process communication
- What it does: Ensures data gets from a specific application/service on the source device to the correct application/service on the destination device
- Key point: It handles the "last mile" delivery to the right application

Analogy: IP gets a letter to the correct apartment building. The Transport Layer gets the letter to the correct person (or apartment number) inside that building.

When you have trouble deciding which direction you are going

<!-- image -->

## How does it know which program to go to?

## Ports!

- A port is just a 16-bit number (0-65535) used to identify a specific application process.
- An IP Address + a Port Number = a unique destination.
- Example Well-Known Ports:
- HTTP (Websites): Port 80
- HTTPS (Secure Websites): Port 443
- FTP (File Transfer): Port 21
- DNS (Domain Name System): Port 53

me: *shuts port*

can't have a network problem if there is no network

<!-- image -->

## Meet the Protocols: TCP &amp; UDP

The Transport Layer has two main "messengers" (protocols) you can choose from. They have very different ways of getting the job done. Choosing the right one is crucial for application performance.

TCP

<!-- image -->

- -Has to connect
- Waits if network is congested
- Sends everything in order

UDP

- Doesn't connect 一
- Doesn't give a shit about networkcongestion
- Doesn't give a single flying fuck about order, he is the ORDER

<!-- image -->

## TCP - The Reliable Messenger

Think of TCP as a registered postal service with tracking and delivery confirmation.

- Connection-Oriented: It establishes a dedicated connection before sending data. This is done via a Three-Way Handshake (SYN, SYN-ACK, ACK).
- Reliable Delivery: Guarantees that data will arrive, and in the correct order. It uses sequence numbers and acknowledgements (ACKs). If a piece of data gets lost, it's re-sent.
- Flow Control: Ensures a sender doesn't overwhelm a receiver with too much data at once.

Congestion Control: Helps prevent the entire network from getting clogged up.

A TCP/IP packet goes into bar. It says, "I'd like a beer" Thet barman asks, "Abeer?' Thep "Yes, packet tresponds, a beer.

<!-- image -->

## When to use TCP?

When you need every piece of data to arrive correctly.

- Web Browsing (HTTP/S)
- Email (SMTP, IMAP)
- File Transfers (FTP)

<!-- image -->

## UDP - The Speedy Messenger

Think of UDP as a standard postcard. You write it, you send it, and you hope for the best.

- Connectionless: No handshake, no pre-existing connection. You just send the data. It's "fire and forget."
- Unreliable: No guarantees.
- Packets (datagrams) might get lost.
- They might arrive out of order.
- They might arrive duplicated.

Very Low Overhead: Because it doesn't do all the extra work of TCP, it's very fast and lightweight.

## When to use UDP?

When speed is more important than perfect accuracy. A small amount of data loss is acceptable.

- Live Video/Audio Streaming: Losing a single frame or a millisecond of audio is better than pausing the whole stream to wait for a lost packet.
- Online Gaming: You need the latest game state now. Old data is useless.

## UDPDatagram HeaderFormat

|   Bit# | 0 7         | 8 15        | 16                      | 23 24                   |
|--------|-------------|-------------|-------------------------|-------------------------|
|      0 | Source Port | Source Port | Destination Port        | Destination Port        |
|     32 | Length      | Length      | Headerand Data Checksum | Headerand Data Checksum |

## Intro to Socket Programming

How do our applications actually use TCP or UDP?

## Through Sockets!

- A socket is one endpoint of a two-way communication link between two programs running on the network.
- It's an API (Application Programming Interface) that lets our code send and receive data over the network.
- When you create a socket, you specify whether you want to use TCP or UDP

## Socket Programming: Conceptual Flow

| Step   | Server Side                                | Client Side                              |
|--------|--------------------------------------------|------------------------------------------|
| 1      | socket() -- Create a new socket            | socket() - Create a new socket           |
| 2      | bind() - Assign IP address and port        | connect() - Connect to server            |
| 3      | listen() - Listen for incoming connections |                                          |
| 4      | accept() - Accept client connection        |                                          |
| 5      | recv() / send() - Communicate with client  | send()  recv() - Communicate with server |
|        | close() - Close the client connection      | close() - Close the connection           |

Questions?