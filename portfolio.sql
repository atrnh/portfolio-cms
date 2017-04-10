--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE categories (
    id integer NOT NULL,
    title character varying(100),
    "desc" text
);


ALTER TABLE categories OWNER TO ashley;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE categories_id_seq OWNER TO ashley;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE categories_id_seq OWNED BY categories.id;


--
-- Name: categories_projects; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE categories_projects (
    id integer NOT NULL,
    category_id integer,
    project_id integer
);


ALTER TABLE categories_projects OWNER TO ashley;

--
-- Name: categories_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE categories_projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE categories_projects_id_seq OWNER TO ashley;

--
-- Name: categories_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE categories_projects_id_seq OWNED BY categories_projects.id;


--
-- Name: media; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE media (
    id integer NOT NULL,
    title character varying(100),
    "desc" text,
    date_updated timestamp with time zone DEFAULT now(),
    source_url character varying(70),
    thumbnail_id integer
);


ALTER TABLE media OWNER TO ashley;

--
-- Name: media_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE media_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE media_id_seq OWNER TO ashley;

--
-- Name: media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE media_id_seq OWNED BY media.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE projects (
    id integer NOT NULL,
    title character varying(100),
    "desc" text,
    date_created date,
    date_updated timestamp with time zone DEFAULT now(),
    main_img_id integer
);


ALTER TABLE projects OWNER TO ashley;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_id_seq OWNER TO ashley;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE projects_id_seq OWNED BY projects.id;


--
-- Name: projects_media; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE projects_media (
    id integer NOT NULL,
    project_id integer,
    media_id integer
);


ALTER TABLE projects_media OWNER TO ashley;

--
-- Name: projects_media_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE projects_media_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_media_id_seq OWNER TO ashley;

--
-- Name: projects_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE projects_media_id_seq OWNED BY projects_media.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE tags (
    code character varying(50) NOT NULL
);


ALTER TABLE tags OWNER TO ashley;

--
-- Name: tags_projects; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE tags_projects (
    id integer NOT NULL,
    project_id integer,
    tag_code character varying(50)
);


ALTER TABLE tags_projects OWNER TO ashley;

--
-- Name: tags_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE tags_projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tags_projects_id_seq OWNER TO ashley;

--
-- Name: tags_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE tags_projects_id_seq OWNED BY tags_projects.id;


--
-- Name: thumbnails; Type: TABLE; Schema: public; Owner: ashley; Tablespace: 
--

CREATE TABLE thumbnails (
    id integer NOT NULL,
    source_url character varying(70)
);


ALTER TABLE thumbnails OWNER TO ashley;

--
-- Name: thumbnails_id_seq; Type: SEQUENCE; Schema: public; Owner: ashley
--

CREATE SEQUENCE thumbnails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE thumbnails_id_seq OWNER TO ashley;

--
-- Name: thumbnails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ashley
--

ALTER SEQUENCE thumbnails_id_seq OWNED BY thumbnails.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY categories ALTER COLUMN id SET DEFAULT nextval('categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY categories_projects ALTER COLUMN id SET DEFAULT nextval('categories_projects_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY media ALTER COLUMN id SET DEFAULT nextval('media_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY projects ALTER COLUMN id SET DEFAULT nextval('projects_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY projects_media ALTER COLUMN id SET DEFAULT nextval('projects_media_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY tags_projects ALTER COLUMN id SET DEFAULT nextval('tags_projects_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY thumbnails ALTER COLUMN id SET DEFAULT nextval('thumbnails_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY categories (id, title, "desc") FROM stdin;
3	Lydia	Test another category of cool photos.
30	Whoooo	\N
1	Testing	This is a test category.
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('categories_id_seq', 30, true);


--
-- Data for Name: categories_projects; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY categories_projects (id, category_id, project_id) FROM stdin;
33	30	5
37	3	13
40	30	11
49	1	3
\.


--
-- Name: categories_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('categories_projects_id_seq', 49, true);


--
-- Data for Name: media; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY media (id, title, "desc", date_updated, source_url, thumbnail_id) FROM stdin;
1	Test Image	This is a test image.	2017-04-01 13:51:15.9175-07	test.jpg	\N
2	Test Cat	Test image of a cat.	2017-04-01 13:51:15.9175-07	cat.jpg	\N
3	Test Sculpture	A test sculpture.	2017-04-01 13:51:15.9175-07	sculpture.jpg	\N
4	Cool Test	Another fake, test image.	2017-04-01 13:51:15.9175-07	cool.jpg	\N
\.


--
-- Name: media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('media_id_seq', 4, true);


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY projects (id, title, "desc", date_created, date_updated, main_img_id) FROM stdin;
4	New project	here is a new project	\N	2017-04-04 14:58:37.767358-07	\N
1	A really cool project	This is a test wow	\N	2017-04-06 16:07:47.07568-07	\N
12	A cool projec	\N	\N	2017-04-06 16:36:23.027391-07	\N
5	A super duper new project	welkjaf;lkw	\N	2017-04-06 17:18:23.211426-07	\N
13	Yahoo	yayyyyyyyy	\N	2017-04-06 17:23:14.497066-07	\N
11	Dund	eogamedunkey	\N	2017-04-06 17:29:04.034258-07	\N
3	Cool Dog	Test project about cool dogs.	\N	2017-04-10 12:46:40.685807-07	\N
\.


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('projects_id_seq', 13, true);


--
-- Data for Name: projects_media; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY projects_media (id, project_id, media_id) FROM stdin;
1	1	1
4	3	3
5	3	4
\.


--
-- Name: projects_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('projects_media_id_seq', 5, true);


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY tags (code) FROM stdin;
test-tag
animals
whee
me
yeah
what
game
fun
pokemon
cool
stuff
dog
sunglasses
\.


--
-- Data for Name: tags_projects; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY tags_projects (id, project_id, tag_code) FROM stdin;
7	11	animals
13	1	animals
14	1	cool
15	1	pokemon
16	1	stuff
17	12	stuff
18	13	stuff
19	13	pokemon
22	3	cool
23	3	dog
24	3	sunglasses
\.


--
-- Name: tags_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('tags_projects_id_seq', 24, true);


--
-- Data for Name: thumbnails; Type: TABLE DATA; Schema: public; Owner: ashley
--

COPY thumbnails (id, source_url) FROM stdin;
1	test_thumb.jpg
2	cat_thumb.jpg
3	sculpture_thumb.jpg
4	cool_thumb.jpg
\.


--
-- Name: thumbnails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ashley
--

SELECT pg_catalog.setval('thumbnails_id_seq', 4, true);


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: categories_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY categories_projects
    ADD CONSTRAINT categories_projects_pkey PRIMARY KEY (id);


--
-- Name: media_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);


--
-- Name: projects_media_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY projects_media
    ADD CONSTRAINT projects_media_pkey PRIMARY KEY (id);


--
-- Name: projects_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: tags_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (code);


--
-- Name: tags_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY tags_projects
    ADD CONSTRAINT tags_projects_pkey PRIMARY KEY (id);


--
-- Name: thumbnails_pkey; Type: CONSTRAINT; Schema: public; Owner: ashley; Tablespace: 
--

ALTER TABLE ONLY thumbnails
    ADD CONSTRAINT thumbnails_pkey PRIMARY KEY (id);


--
-- Name: categories_projects_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY categories_projects
    ADD CONSTRAINT categories_projects_category_id_fkey FOREIGN KEY (category_id) REFERENCES categories(id);


--
-- Name: categories_projects_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY categories_projects
    ADD CONSTRAINT categories_projects_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(id);


--
-- Name: media_thumbnail_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY media
    ADD CONSTRAINT media_thumbnail_id_fkey FOREIGN KEY (thumbnail_id) REFERENCES thumbnails(id);


--
-- Name: projects_main_img_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY projects
    ADD CONSTRAINT projects_main_img_id_fkey FOREIGN KEY (main_img_id) REFERENCES media(id);


--
-- Name: projects_media_media_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY projects_media
    ADD CONSTRAINT projects_media_media_id_fkey FOREIGN KEY (media_id) REFERENCES media(id);


--
-- Name: projects_media_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY projects_media
    ADD CONSTRAINT projects_media_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(id);


--
-- Name: tags_projects_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY tags_projects
    ADD CONSTRAINT tags_projects_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(id);


--
-- Name: tags_projects_tag_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ashley
--

ALTER TABLE ONLY tags_projects
    ADD CONSTRAINT tags_projects_tag_code_fkey FOREIGN KEY (tag_code) REFERENCES tags(code);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

