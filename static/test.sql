CREATE TABLE public.cabinets (
    place_id text NOT NULL,
    name text,
    formatted_address text,
    rating text,
    geometry text,
    temp_distance text
);


CREATE TABLE public.user_search_history (
    user_email text NOT NULL,
    search_text text NOT NULL
);


CREATE TABLE public.users (
    email text NOT NULL,
    premium_expiration date
);



INSERT INTO public.cabinets VALUES ('ChIJ1wEkwmUDskARjwjAEn6zObw', 'Gema Clinic', 'Calea Mosilor 158 Mosilor Office Building, parter 030167', '5', '44.4372888,26.1135536', '0.21398611484422855');
INSERT INTO public.cabinets VALUES ('ChIJf1FQma74sUARWaugdoKMbrg', 'Nativia', 'Strada Pitar Moș nr. 12, București 030167', '4.8', '44.4424822,26.1011366', '0.9814221715492225');
INSERT INTO public.cabinets VALUES ('ChIJVVUxeMz4sUARg1--amrk1SM', 'CABINET PARTICULAR ORL ACUPUNCTURA SI LASERTERAPIE', 'Calea Moșilor 245, București', '4.6', '44.4420873,26.109142', '0.42969621840677724');
INSERT INTO public.cabinets VALUES ('ChIJm-BmuTP_sUAR5CF2CvG2qLo', 'Dentalis Art Concept', 'Strada Rumeoara 27, București 024064', '5', '44.44154,26.119182', '0.5989101909597944');
INSERT INTO public.cabinets VALUES ('ChIJH3wdQbf4sUARlHhZHViP_4o', 'SORA DINU', 'Str. Grozovici Calistrat,Dr., 6, Bucuresti-Sector 2, Bucuresti, 21105, București', '0', '44.45464,26.11548', '1.7473086037880152');


INSERT INTO public.user_search_history VALUES ('robertchiriac196@gmail.com', 'search_string');
INSERT INTO public.user_search_history VALUES ('robertchiriac196@gmail.com', 'dentist');


INSERT INTO public.users VALUES ('robertchiriac196@gmail.com', '2022-12-17');



ALTER TABLE ONLY public.cabinets
    ADD CONSTRAINT cabinets_pkey PRIMARY KEY (place_id);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (email);


=

ALTER TABLE ONLY public.user_search_history
    ADD CONSTRAINT user_search_history_user_email_fkey FOREIGN KEY (user_email) REFERENCES public.users(email);


