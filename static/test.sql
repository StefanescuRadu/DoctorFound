--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5
-- Dumped by pg_dump version 14.1

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

ALTER TABLE ONLY public.user_search_history DROP CONSTRAINT user_search_history_user_email_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.cabinets DROP CONSTRAINT cabinets_pkey;
DROP TABLE public.users;
DROP TABLE public.user_search_history;
DROP TABLE public.cabinets;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cabinets; Type: TABLE; Schema: public; Owner: robert
--

CREATE TABLE public.cabinets (
    place_id text NOT NULL,
    name text,
    formatted_address text,
    rating text,
    geometry text,
    temp_distance text
);


ALTER TABLE public.cabinets OWNER TO robert;

--
-- Name: user_search_history; Type: TABLE; Schema: public; Owner: robert
--

CREATE TABLE public.user_search_history (
    user_email text NOT NULL,
    search_text text NOT NULL
);


ALTER TABLE public.user_search_history OWNER TO robert;

--
-- Name: users; Type: TABLE; Schema: public; Owner: robert
--

CREATE TABLE public.users (
    email text NOT NULL,
    premium_expiration date
);


ALTER TABLE public.users OWNER TO robert;

--
-- Data for Name: cabinets; Type: TABLE DATA; Schema: public; Owner: robert
--

INSERT INTO public.cabinets VALUES ('ChIJ1wEkwmUDskARjwjAEn6zObw', 'Gema Clinic', 'Calea Mosilor 158 Mosilor Office Building, parter 030167', '5', '44.4372888,26.1135536', '0.21398611484422855');
INSERT INTO public.cabinets VALUES ('ChIJf1FQma74sUARWaugdoKMbrg', 'Nativia', 'Strada Pitar Moș nr. 12, București 030167', '4.8', '44.4424822,26.1011366', '0.9814221715492225');
INSERT INTO public.cabinets VALUES ('ChIJVVUxeMz4sUARg1--amrk1SM', 'CABINET PARTICULAR ORL ACUPUNCTURA SI LASERTERAPIE', 'Calea Moșilor 245, București', '4.6', '44.4420873,26.109142', '0.42969621840677724');
INSERT INTO public.cabinets VALUES ('ChIJm-BmuTP_sUAR5CF2CvG2qLo', 'Dentalis Art Concept', 'Strada Rumeoara 27, București 024064', '5', '44.44154,26.119182', '0.5989101909597944');
INSERT INTO public.cabinets VALUES ('ChIJH3wdQbf4sUARlHhZHViP_4o', 'SORA DINU', 'Str. Grozovici Calistrat,Dr., 6, Bucuresti-Sector 2, Bucuresti, 21105, București', '0', '44.45464,26.11548', '1.7473086037880152');


--
-- Data for Name: user_search_history; Type: TABLE DATA; Schema: public; Owner: robert
--

INSERT INTO public.user_search_history VALUES ('robertchiriac196@gmail.com', 'search_string');
INSERT INTO public.user_search_history VALUES ('robertchiriac196@gmail.com', 'dentist');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: robert
--

INSERT INTO public.users VALUES ('robertchiriac196@gmail.com', '2022-12-17');


--
-- Name: cabinets cabinets_pkey; Type: CONSTRAINT; Schema: public; Owner: robert
--

ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_pkey PRIMARY KEY (place_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: robert
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


--
-- Name: user_search_history user_search_history_user_email_fkey; Type: FK CONSTRAINT; Schema: public; Owner: robert
--

ALTER TABLE ONLY public.user_search_history
    ADD CONSTRAINT user_search_history_user_email_fkey FOREIGN KEY (user_email) REFERENCES public.users(email);


--
-- PostgreSQL database dump complete
--

