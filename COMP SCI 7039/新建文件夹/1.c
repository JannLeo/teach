#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "emulator.h"
#include "sr.h"

/* ******************************************************************
   Go Back N protocol.  Adapted from J.F.Kurose
   ALTERNATING BIT AND GO-BACK-N NETWORK EMULATOR: VERSION 1.2  

   Network properties:
   - one way network delay averages five time units (longer if there
   are other messages in the channel for GBN), but can be larger
   - packets can be corrupted (either the header or the data portion)
   or lost, according to user-defined probabilities
   - packets will be delivered in the order in which they were sent
   (although some can be lost).

   Modifications: 
   - removed bidirectional GBN code and other code not used by prac. 
   - fixed C style to adhere to current programming style
   - added GBN implementation
**********************************************************************/

#define RTT  16.0       /* round trip time.  MUST BE SET TO 16.0 when submitting assignment */
#define WINDOWSIZE 6    /* the maximum number of buffered unacked packet */
#define SEQSPACE 12      /* the min sequence space for GBN must be at least windowsize + 1 */
#define NOTINUSE (-1)   /* used to fill header fields that are not being used */

/* generic procedure to compute the checksum of a packet.  Used by both sender and receiver  
   the simulator will overwrite part of your packet with 'z's.  It will not overwrite your 
   original checksum.  This procedure must generate a different checksum to the original if
   the packet is corrupted.
*/

static struct pkt buffer[SEQSPACE];
static bool acked[SEQSPACE];

static int base = 0;
static int A_nextseqnum = 0;


int ComputeChecksum(struct pkt packet)
{
  int checksum = 0;
  int i;

  checksum = packet.seqnum;
  checksum += packet.acknum;
  for ( i=0; i<20; i++ ) 
    checksum += (int)(packet.payload[i]);

  return checksum;
}

bool IsCorrupted(struct pkt packet)
{
  if (packet.checksum == ComputeChecksum(packet))
    return (false);
  else
    return (true);
}

bool IsInWindow(int seq, int base, int size) {
    return ((seq >= base && seq < base + size) ||
            (base + size >= SEQSPACE && (seq < (base + size) % SEQSPACE || seq >= base)));
}

/* called from layer 5 (application layer), passed the message to be sent to other side */
void A_output(struct msg message)
{
    struct pkt sendpkt;
    int i;

    if ((A_nextseqnum + SEQSPACE - base) % SEQSPACE < WINDOWSIZE) {
        if (TRACE > 1)
        printf("----A: New message arrives, send window is not full, send new messge to layer3!\n");

        sendpkt.seqnum = A_nextseqnum;
        sendpkt.acknum = NOTINUSE;
        for (i = 0; i < 20; i++)
            sendpkt.payload[i] = message.data[i];
        sendpkt.checksum = ComputeChecksum(sendpkt);

        buffer[A_nextseqnum] = sendpkt;
        acked[A_nextseqnum] = false;

        tolayer3(A, sendpkt);
        if (TRACE > 0)
            printf("Sending packet %d to layer 3\n", sendpkt.seqnum);

        if (base == A_nextseqnum) {
            starttimer(A, RTT);
        }

        A_nextseqnum = (A_nextseqnum + 1) % SEQSPACE;
    } else {
        if (TRACE > 0)
            printf("----A: New message arrives, send window is full\n");
        window_full++;
    }
}



/* called from layer 3, when a packet arrives for layer 4 
   In this practical this will always be an ACK as B never sends data.
*/
void A_input(struct pkt packet)
{
    int acknum = packet.acknum;

    if (!IsCorrupted(packet)) {
        if (TRACE > 0)
            printf("----A: uncorrupted ACK %d is received\n", acknum);
        total_ACKs_received++;

        if (!acked[acknum]) {
            if (TRACE > 0)
                printf("----A: ACK %d is not a duplicate\n", acknum);
            new_ACKs++;

            acked[acknum] = true;

            /* move base forward if possible */
            while (acked[base]) {
                acked[base] = false;
                base = (base + 1) % SEQSPACE;
            }

            /* manage timer */
            stoptimer(A);
            if (base != A_nextseqnum) {
                starttimer(A, RTT);
            }
        } else {
            if (TRACE > 0)
                printf("----A: duplicate ACK received, do nothing!\n");
        }
    } else {
        if (TRACE > 0)
            printf("----A: corrupted ACK is received, do nothing!\n");
    }
}

/* called when A's timer goes off */
void A_timerinterrupt(void)
{
    if (TRACE > 0)
        printf("----A: timeout, resending all unACKed packets in window\n");

    int i = base;
    while (i != A_nextseqnum) {
        if (!acked[i]) {
            if (TRACE > 0)
                printf("----A: resending packet %d\n", i);
            tolayer3(A, buffer[i]);
            packets_resent++;
        }
        i = (i + 1) % SEQSPACE;
    }

    starttimer(A, RTT);
}


/* the following routine will be called once (only) before any other */
/* entity A routines are called. You can use it to do any initialization */
void A_init(void)
{
  int i;
  /* initialise A's window, buffer and sequence number */
  A_nextseqnum = 0;  /* A starts with seq num 0, do not change this */
  base = 0;
  for (i = 0; i < SEQSPACE; i++) {
    acked[i] = false;
  }
}



/********* Receiver (B)  variables and procedures ************/

static int expectedseqnum; /* the sequence number expected next by the receiver */
static bool received[SEQSPACE];
static struct pkt recv_buffer[SEQSPACE];

/* called from layer 3, when a packet arrives for layer 4 at B*/
/* called from layer 3, when a packet arrives for layer 4 at B */
void B_input(struct pkt packet)
{
    struct pkt ackpkt;
    int i;
    int seq = packet.seqnum;

    if (!IsCorrupted(packet)) {
        if (TRACE > 0)
            printf("----B: packet %d is correctly received, send ACK!\n", seq);
        
        packets_received++;

        if (IsInWindow(seq, expectedseqnum, WINDOWSIZE))
        {

            if (!received[seq]) {
                if (TRACE > 0) {
                    if (seq == expectedseqnum)
                        printf("----B: packet %d is expected, deliver immediately\n", seq);
                    else
                        printf("----B: packet %d is out-of-order, buffered\n", seq);
                }
                recv_buffer[seq] = packet;
                received[seq] = true;
            }
            ackpkt.seqnum = 0;
            ackpkt.acknum = seq;
            for (i = 0; i < 20; i++)
                ackpkt.payload[i] = '0';
            ackpkt.checksum = ComputeChecksum(ackpkt);
            tolayer3(B, ackpkt);

            while (received[expectedseqnum]) {
                tolayer5(B, recv_buffer[expectedseqnum].payload);
                received[expectedseqnum] = false;
                expectedseqnum = (expectedseqnum + 1) % SEQSPACE;
            }
        }
        else {
            if (TRACE > 0)
                printf("----B: packet %d not in window, ignored\n", seq);
        }
    }
    else {
        if (TRACE > 0)
            printf("----B: corrupted packet received, ignored\n");
    }
}


/* the following routine will be called once (only) before any other */
/* entity B routines are called. You can use it to do any initialization */
void B_init(void)
{
    int i;
    expectedseqnum = 0;
    for (i = 0; i < SEQSPACE; i++) {
        received[i] = false;
    }
}

/******************************************************************************
 * The following functions need be completed only for bi-directional messages *
 *****************************************************************************/

/* Note that with simplex transfer from a-to-B, there is no B_output() */
void B_output(struct msg message)  
{
}

/* called when B's timer goes off */
void B_timerinterrupt(void)
{
}