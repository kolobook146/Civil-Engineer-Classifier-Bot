# Stage 23: Payment / Commercial Engine Report

## Scope

This report studies payment and commercial-management systems as a full extension family.

Primary evidence base:

- `SRC-A-105`
- `SRC-A-106`
- `SRC-A-126`
- `SRC-A-130`
- `SRC-A-131`
- `SRC-A-134`
- `SRC-A-139`
- `SRC-A-146`
- `SRC-A-147`
- `SRC-A-148`

## Main Conclusion

Payment and commercial systems are not financial notes attached to tasks.
They are governed engines for:

- commitments and contracts;
- schedules of values;
- invoices and payment applications;
- change events and change orders;
- holds and releases;
- compliance documents;
- reconciliation and proof of payment.

Research interpretation:
this is the strongest `decomposition + governance + legal-financial control` family in Stage 23.

## Core Commercial Object Model

The recurring object model is:

- contract or commitment;
- billing package or draw;
- schedule-of-values line;
- requisition or invoice;
- change event or change request;
- change order;
- retainage;
- compliance document or waiver;
- payment hold;
- payment record or disbursement;
- reconciliation report.

## Strong Evidence from Software Documentation

### Oracle Textura

`SRC-A-146`, `SRC-A-147`, and `SRC-A-148` provide one of the clearest open commercial-control grammars:

- subcontractor payment application workflow;
- compliance management;
- automatic or rules-based holds;
- held-payment reporting;
- legal-document and waiver logic;
- downstream payment visibility.

This is important because it proves that payment state is not just `approved / paid`.
It often depends on compliance, holds, and supporting documentation.

### Oracle Unifier

`SRC-A-126` shows payment-commercial behavior inside PMIS:

- cost-type business processes;
- schedule-of-values handling;
- payment applications;
- commitment-aware cost forms.

### PMWeb

`SRC-A-130`, `SRC-A-131`, and `SRC-A-133` show a similar integrated grammar:

- requisitions;
- linked change events;
- contract and revenue logic;
- percent-complete support;
- commercial workflow records.

### Procore

`SRC-A-139` shows collaborative commercial objects:

- progress billings;
- owner invoices;
- invoice contacts;
- SOV-linked invoice behavior;
- held-payment visibility in broader Procore financial workflows.

## Regional and Enterprise Signals

### Middle East

Middle East owner practice remains one of the strongest environments for payment-linked controls:

- PMIS and payment processes are often tightly coupled;
- cost-loaded master schedules and payment controls coexist;
- contractor KPI, change, and payment governance are explicit.

### USA and global contractor / owner market

The U.S.-led commercial software evidence is especially strong on:

- subcontractor billing;
- lien or legal-document compliance;
- downstream payment visibility;
- change and invoice traceability.

## Relationship to Schedule

The payment / commercial engine is schedule-adjacent in several different ways:

1. valuation is often tied to progress or percent complete;
2. payment milestones and billing periods shape delivery behavior;
3. change events alter cost and sometimes time obligations;
4. payment holds may affect execution if cash flow is delayed;
5. owner-side controls often compare schedule status and billing status together.

But commercial state still cannot be collapsed into schedule state.

## Why It Stays Outside the Pilot Core

A full commercial subsystem would require dedicated handling of:

- billing periods;
- SOV mathematics;
- retainage;
- compliance holds;
- disbursement and reconciliation;
- change-to-payment traceability.

That is justified in mature enterprise delivery systems, but too heavy for the present pilot core.

## Target-Model Implication

The current model should preserve:

- payment events as schedule items where needed;
- governance records for billing, hold, and approval outcomes;
- external object links to commercial records;
- coding support for contract package, commitment, and SOV context.

It should not yet absorb:

- invoice line-detail logic;
- draw workflow state;
- automatic commercial calculations;
- legal-document and waiver engines.

## Bottom-Line Result

Payment / commercial management is one of the most structurally complete extension families in the Stage 23 corpus.
If the project later moves from schedule-centric control into contractual execution control, this subsystem is a prime candidate for dedicated expansion.
