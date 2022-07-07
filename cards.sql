--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-2.pgdg20.04+1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-2.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.sent_cards DROP CONSTRAINT sent_cards_contact_id_fkey;
ALTER TABLE ONLY public.sent_cards DROP CONSTRAINT sent_cards_card_id_fkey;
ALTER TABLE ONLY public.contacts DROP CONSTRAINT contacts_user_id_fkey;
ALTER TABLE ONLY public.cards DROP CONSTRAINT cards_user_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY public.sent_cards DROP CONSTRAINT sent_cards_pkey;
ALTER TABLE ONLY public.contacts DROP CONSTRAINT contacts_pkey;
ALTER TABLE ONLY public.cards DROP CONSTRAINT cards_pkey;
ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE public.sent_cards ALTER COLUMN sent_card_id DROP DEFAULT;
ALTER TABLE public.contacts ALTER COLUMN contact_id DROP DEFAULT;
ALTER TABLE public.cards ALTER COLUMN card_id DROP DEFAULT;
DROP SEQUENCE public.users_user_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.sent_cards_sent_card_id_seq;
DROP TABLE public.sent_cards;
DROP SEQUENCE public.contacts_contact_id_seq;
DROP TABLE public.contacts;
DROP SEQUENCE public.cards_card_id_seq;
DROP TABLE public.cards;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cards (
    card_id integer NOT NULL,
    title character varying,
    url character varying,
    published boolean,
    tags character varying,
    hidden boolean,
    user_id integer
);


--
-- Name: cards_card_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cards_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cards_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cards_card_id_seq OWNED BY public.cards.card_id;


--
-- Name: contacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contacts (
    contact_id integer NOT NULL,
    recipient character varying,
    phone_number character varying,
    email character varying,
    hidden boolean,
    user_id integer
);


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contacts_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contacts_contact_id_seq OWNED BY public.contacts.contact_id;


--
-- Name: sent_cards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sent_cards (
    sent_card_id integer NOT NULL,
    message text,
    date_sent timestamp without time zone,
    card_id integer,
    contact_id integer
);


--
-- Name: sent_cards_sent_card_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sent_cards_sent_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sent_cards_sent_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sent_cards_sent_card_id_seq OWNED BY public.sent_cards.sent_card_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying,
    password character varying
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: cards card_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cards ALTER COLUMN card_id SET DEFAULT nextval('public.cards_card_id_seq'::regclass);


--
-- Name: contacts contact_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts ALTER COLUMN contact_id SET DEFAULT nextval('public.contacts_contact_id_seq'::regclass);


--
-- Name: sent_cards sent_card_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sent_cards ALTER COLUMN sent_card_id SET DEFAULT nextval('public.sent_cards_sent_card_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: cards; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cards (card_id, title, url, published, tags, hidden, user_id) FROM stdin;
1	Ruff life	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/rqkir4aiyminpucjmqdo.jpg	t	frenchie, french bulldog, champion shirt, yellow, ruff life	t	1
34	Ruff life	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/nhz8lj1rycqd4tgnkxfl.jpg	f	\N	f	1
68	Ruff life	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/rqkir4aiyminpucjmqdo.jpg	f	\N	t	1
67	Puppy	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/co2q7p3id4jljfh3tzkj.jpg	f	\N	f	1
69	cat tongue	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/vzyjy9mmekrqohlwuojr.jpg	f	\N	f	1
70	Phunky Heart	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/ulceauwfi4y901a6xtiz.jpg	f	\N	f	1
71	Humming Along	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/m12kxpoo2x8a3kxhq3jj.jpg	t	humming along, hummingbird, bird, flying, wings, beak, flapping	f	1
72	Tiger	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/s96einadpbmuse8of7iq.jpg	t	Tiger, river, swimming	f	1
73	Tiger	http://res.cloudinary.com/dejqcmvuw/image/upload/c_fill,h_400,w_600/s96einadpbmuse8of7iq.jpg	f	\N	t	1
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contacts (contact_id, recipient, phone_number, email, hidden, user_id) FROM stdin;
1	Ginger Wu	6266366223	gingercw@gmail.com	t	1
2	Ginger Wu	6266366223	gingercw@gmail.com	f	1
3	Chengfeng Ren	6266366223	chengfengren@gmail.com	f	1
4	Derrick Wu	6266366223		f	1
5	Lauren	6266366223	laurenpritchett2@gmail.com	f	1
\.


--
-- Data for Name: sent_cards; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sent_cards (sent_card_id, message, date_sent, card_id, contact_id) FROM stdin;
1	Hi! Here's a dog.	2022-06-26 01:43:36	34	2
2	Hi Chengfeng! Hope you are doing as well as this puppy.	2022-06-28 01:39:45	67	3
3	Hi Lauren! You are the cat's meow!	2022-07-01 17:14:05	69	5
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, email, password) FROM stdin;
1	test_email@yahoo.com	hello
\.


--
-- Name: cards_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cards_card_id_seq', 73, true);


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contacts_contact_id_seq', 5, true);


--
-- Name: sent_cards_sent_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sent_cards_sent_card_id_seq', 3, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: cards cards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (card_id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (contact_id);


--
-- Name: sent_cards sent_cards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sent_cards
    ADD CONSTRAINT sent_cards_pkey PRIMARY KEY (sent_card_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: cards cards_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: contacts contacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: sent_cards sent_cards_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sent_cards
    ADD CONSTRAINT sent_cards_card_id_fkey FOREIGN KEY (card_id) REFERENCES public.cards(card_id);


--
-- Name: sent_cards sent_cards_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sent_cards
    ADD CONSTRAINT sent_cards_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contacts(contact_id);


--
-- PostgreSQL database dump complete
--

