--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: lt_domain; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_domain (
    id integer NOT NULL,
    pid integer,
    domain_name character varying(65) NOT NULL,
    project_id integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE lt_domain OWNER TO "www-data";

--
-- Name: lt_domain_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_domain_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_domain_id_seq OWNER TO "www-data";

--
-- Name: lt_domain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_domain_id_seq OWNED BY lt_domain.id;


--
-- Name: lt_license; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_license (
    id integer NOT NULL,
    license_abbrev character varying(20) NOT NULL,
    license_name character varying(255) NOT NULL,
    legal_text character varying,
    text_url character varying(255),
    access boolean NOT NULL,
    share boolean NOT NULL,
    edit boolean NOT NULL,
    commercial boolean NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_license_check CHECK (((legal_text IS NOT NULL) OR (text_url IS NOT NULL)))
);


ALTER TABLE lt_license OWNER TO "www-data";

--
-- Name: lt_license_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_license_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_license_id_seq OWNER TO "www-data";

--
-- Name: lt_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_license_id_seq OWNED BY lt_license.id;


--
-- Name: lt_location; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_location (
    id integer NOT NULL,
    centroid_x numeric,
    centroid_y numeric,
    srid integer,
    geometry_type character varying(15),
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    geom geometry NOT NULL
);


ALTER TABLE lt_location OWNER TO "www-data";

--
-- Name: lt_location_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_location_id_seq OWNER TO "www-data";

--
-- Name: lt_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_location_id_seq OWNED BY lt_location.id;


--
-- Name: lt_project; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_project (
    id integer NOT NULL,
    project_name character varying(65) NOT NULL,
    user_id integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE lt_project OWNER TO "www-data";

--
-- Name: lt_project_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_project_id_seq OWNER TO "www-data";

--
-- Name: lt_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_project_id_seq OWNED BY lt_project.id;


--
-- Name: lt_quality; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_quality (
    id integer NOT NULL,
    flag_name character varying(25) NOT NULL,
    flag_weight integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_quality_flag_weight_check CHECK ((flag_weight >= 0)),
    CONSTRAINT lt_quality_flag_weight_check1 CHECK ((flag_weight <= 100))
);


ALTER TABLE lt_quality OWNER TO "www-data";

--
-- Name: lt_quality_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_quality_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_quality_id_seq OWNER TO "www-data";

--
-- Name: lt_quality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_quality_id_seq OWNED BY lt_quality.id;


--
-- Name: lt_site; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_site (
    id integer NOT NULL,
    site_name character varying(65),
    elevation numeric,
    rel_height numeric,
    orientation_degree integer,
    slope numeric,
    landuse character varying(65),
    site_comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_site_orientation_degree_check CHECK ((orientation_degree >= 0)),
    CONSTRAINT lt_site_orientation_degree_check1 CHECK ((orientation_degree <= 360)),
    CONSTRAINT lt_site_slope_check CHECK ((slope >= (0)::numeric)),
    CONSTRAINT lt_site_slope_check1 CHECK ((slope < (1)::numeric))
);


ALTER TABLE lt_site OWNER TO "www-data";

--
-- Name: lt_site_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_site_id_seq OWNER TO "www-data";

--
-- Name: lt_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_site_id_seq OWNED BY lt_site.id;


--
-- Name: lt_soil; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_soil (
    id integer NOT NULL,
    geology character varying(65),
    soil_type character varying(65),
    porosity numeric,
    field_capacity numeric,
    residual_moisture numeric,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    CONSTRAINT lt_soil_check CHECK ((field_capacity > residual_moisture)),
    CONSTRAINT lt_soil_check1 CHECK ((field_capacity < porosity)),
    CONSTRAINT lt_soil_check2 CHECK ((residual_moisture < porosity)),
    CONSTRAINT lt_soil_field_capacity_check CHECK (((field_capacity < (1)::numeric) AND (field_capacity > (0)::numeric))),
    CONSTRAINT lt_soil_porosity_check CHECK (((porosity < (1)::numeric) AND (porosity > (0)::numeric))),
    CONSTRAINT lt_soil_residual_moisture_check CHECK (((residual_moisture < (1)::numeric) AND (residual_moisture > (0)::numeric)))
);


ALTER TABLE lt_soil OWNER TO "www-data";

--
-- Name: lt_soil_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_soil_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_soil_id_seq OWNER TO "www-data";

--
-- Name: lt_soil_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_soil_id_seq OWNED BY lt_soil.id;


--
-- Name: lt_source_type; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_source_type (
    id integer NOT NULL,
    type_name character varying(65) NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE lt_source_type OWNER TO "www-data";

--
-- Name: lt_source_type_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_source_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_source_type_id_seq OWNER TO "www-data";

--
-- Name: lt_source_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_source_type_id_seq OWNED BY lt_source_type.id;


--
-- Name: lt_unit; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_unit (
    id integer NOT NULL,
    unit_name character varying(65) NOT NULL,
    unit_abbrev character varying(15) NOT NULL,
    unit_symbol character varying(5) NOT NULL,
    derived_si boolean,
    to_derived_si character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE lt_unit OWNER TO "www-data";

--
-- Name: lt_unit_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_unit_id_seq OWNER TO "www-data";

--
-- Name: lt_unit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_unit_id_seq OWNED BY lt_unit.id;


--
-- Name: lt_user; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE lt_user (
    id integer NOT NULL,
    is_institution boolean NOT NULL,
    first_name character varying(65),
    last_name character varying(65),
    institution_name character varying(255),
    department character varying(255),
    email character varying(60),
    comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE lt_user OWNER TO "www-data";

--
-- Name: lt_user_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE lt_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lt_user_id_seq OWNER TO "www-data";

--
-- Name: lt_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE lt_user_id_seq OWNED BY lt_user.id;


--
-- Name: nm_meta_domain; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE nm_meta_domain (
    meta_id integer,
    domain_id integer
);


ALTER TABLE nm_meta_domain OWNER TO "www-data";

--
-- Name: tbl_data; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE tbl_data (
    tstamp timestamp without time zone NOT NULL,
    meta_id integer NOT NULL,
    value numeric NOT NULL
);


ALTER TABLE tbl_data OWNER TO "www-data";

--
-- Name: tbl_data_source; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE tbl_data_source (
    id integer NOT NULL,
    source_type_id integer,
    source_path character varying NOT NULL,
    settings character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE tbl_data_source OWNER TO "www-data";

--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE tbl_data_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tbl_data_source_id_seq OWNER TO "www-data";

--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE tbl_data_source_id_seq OWNED BY tbl_data_source.id;


--
-- Name: tbl_meta; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE tbl_meta (
    id integer NOT NULL,
    ts_start timestamp without time zone,
    ts_stop timestamp without time zone,
    external_id character varying(255),
    support character varying(255),
    spacing character varying(255),
    creator_id integer,
    publisher_id integer,
    geometry_id integer,
    license_id integer,
    quality_id integer,
    site_id integer,
    soil_id integer,
    variable_id integer,
    sensor_id integer,
    source_id integer,
    comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE tbl_meta OWNER TO "www-data";

--
-- Name: tbl_meta_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE tbl_meta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tbl_meta_id_seq OWNER TO "www-data";

--
-- Name: tbl_meta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE tbl_meta_id_seq OWNED BY tbl_meta.id;


--
-- Name: tbl_sensor; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE tbl_sensor (
    id integer NOT NULL,
    sensor_name character varying(65),
    manufacturer character varying(255),
    documentation_url character varying,
    last_configured timestamp without time zone,
    valid_until timestamp without time zone,
    sensor_comment character varying,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE tbl_sensor OWNER TO "www-data";

--
-- Name: tbl_sensor_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE tbl_sensor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tbl_sensor_id_seq OWNER TO "www-data";

--
-- Name: tbl_sensor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE tbl_sensor_id_seq OWNED BY tbl_sensor.id;


--
-- Name: tbl_variable; Type: TABLE; Schema: public; Owner: "www-data"
--

CREATE TABLE tbl_variable (
    id integer NOT NULL,
    variable_name character varying(65) NOT NULL,
    variable_abbrev character varying(15) NOT NULL,
    variable_symbol character varying(5) NOT NULL,
    unit_id integer NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


ALTER TABLE tbl_variable OWNER TO "www-data";

--
-- Name: tbl_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: "www-data"
--

CREATE SEQUENCE tbl_variable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tbl_variable_id_seq OWNER TO "www-data";

--
-- Name: tbl_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: "www-data"
--

ALTER SEQUENCE tbl_variable_id_seq OWNED BY tbl_variable.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_domain ALTER COLUMN id SET DEFAULT nextval('lt_domain_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_license ALTER COLUMN id SET DEFAULT nextval('lt_license_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_location ALTER COLUMN id SET DEFAULT nextval('lt_location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_project ALTER COLUMN id SET DEFAULT nextval('lt_project_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_quality ALTER COLUMN id SET DEFAULT nextval('lt_quality_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_site ALTER COLUMN id SET DEFAULT nextval('lt_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_soil ALTER COLUMN id SET DEFAULT nextval('lt_soil_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_source_type ALTER COLUMN id SET DEFAULT nextval('lt_source_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_unit ALTER COLUMN id SET DEFAULT nextval('lt_unit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_user ALTER COLUMN id SET DEFAULT nextval('lt_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_data_source ALTER COLUMN id SET DEFAULT nextval('tbl_data_source_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta ALTER COLUMN id SET DEFAULT nextval('tbl_meta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_sensor ALTER COLUMN id SET DEFAULT nextval('tbl_sensor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_variable ALTER COLUMN id SET DEFAULT nextval('tbl_variable_id_seq'::regclass);


--
-- Data for Name: lt_domain; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_domain (id, pid, domain_name, project_id, created_on, updated_on) FROM stdin;
\.


--
-- Name: lt_domain_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_domain_id_seq', 1, false);


--
-- Data for Name: lt_license; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_license (id, license_abbrev, license_name, legal_text, text_url, access, share, edit, commercial, created_on, updated_on) FROM stdin;
1	CC BY 2.0 DE	Namensnennung 2.0 Deutschland	\N	https://creativecommons.org/licenses/by/2.0/de/	t	t	t	t	\N	\N
2	CC BY-ND 3.0 DE	Namensnennung - Keine Bearbeitung 3.0 Deutschland	\N	https://creativecommons.org/licenses/by-nd/3.0/de/	t	t	f	t	\N	\N
3	CC BY-NC 3.0 DE	Namensnennung - Nicht kommerziell 3.0 Deutschland	\N	https://creativecommons.org/licenses/by-nc/3.0/de/	t	t	t	f	\N	\N
4	CC BY-NC-ND 3.0 De	Namensnennung - Nicht kommerziell - Keine Bearbeitung 3.0 Deutschland	\N	https://creativecommons.org/licenses/by-nc-nd/3.0/de/	t	t	f	f	\N	\N
5	CC BY-NC-SA 3.0 DE	Namensnennung - Nicht kommerziell - Weitergabe unter gleichen Bedingungen 3.0 Deutschland	\N	https://creativecommons.org/licenses/by-nc-sa/3.0/de/	t	t	t	f	\N	\N
6	CC BY-SA 3.0 DE	Namensnennung - Weitergabe unter gleichen Bedingungen 3.0 Deutschland	\N	https://creativecommons.org/licenses/by-sa/3.0/de/	t	t	t	t	\N	\N
7	dl-de/by-2-0	Datenlizenz Deutschland - Namensnennung - Version 2.0	\N	https://www.govdata.de/dl-de/by-2-0	t	t	t	t	\N	\N
8	dl-de/zero-2.0	Datenlizenz Deutschland - Zero - Version 2.0	\N	https://www.govdata.de/dl-de/zero-2-0	t	t	t	t	\N	\N
9	dl-de/by-nc-1-0	Datenlizenz Deutschland - Namensnennung . nicht kommerziell - Version 1.0	\N	https://www.govdata.de/dl-de/by-nc-1-0	t	t	t	f	\N	\N
\.


--
-- Name: lt_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_license_id_seq', 9, true);


--
-- Data for Name: lt_location; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_location (id, centroid_x, centroid_y, srid, geometry_type, created_on, updated_on, geom) FROM stdin;
\.


--
-- Name: lt_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_location_id_seq', 1, false);


--
-- Data for Name: lt_project; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_project (id, project_name, user_id, created_on, updated_on) FROM stdin;
1	default	\N	\N	\N
\.


--
-- Name: lt_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_project_id_seq', 1, false);


--
-- Data for Name: lt_quality; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_quality (id, flag_name, flag_weight, created_on, updated_on) FROM stdin;
1	checked	10	\N	\N
2	corrected	30	\N	\N
3	unchecked	50	\N	\N
4	questionable	70	\N	\N
5	faulty	90	\N	\N
\.


--
-- Name: lt_quality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_quality_id_seq', 1, false);


--
-- Data for Name: lt_site; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_site (id, site_name, elevation, rel_height, orientation_degree, slope, landuse, site_comment, created_on, updated_on) FROM stdin;
\.


--
-- Name: lt_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_site_id_seq', 1, false);


--
-- Data for Name: lt_soil; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_soil (id, geology, soil_type, porosity, field_capacity, residual_moisture, created_on, updated_on) FROM stdin;
\.


--
-- Name: lt_soil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_soil_id_seq', 1, false);


--
-- Data for Name: lt_source_type; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_source_type (id, type_name, created_on, updated_on) FROM stdin;
1	internal	\N	\N
2	filepath	\N	\N
3	fileurl	\N	\N
4	wms	\N	\N
5	wfs	\N	\N
6	jsonp	\N	\N
7	database	\N	\N
\.


--
-- Name: lt_source_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_source_type_id_seq', 1, false);


--
-- Data for Name: lt_unit; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_unit (id, unit_name, unit_abbrev, unit_symbol, derived_si, to_derived_si, created_on, updated_on) FROM stdin;
1	Grad Celsius	deg. C	C	\N	\N	\N	\N
2	Prozent	pct.	%	\N	\N	\N	\N
3	Millibar	mbar	mbar	\N	\N	\N	\N
4	Millimeter	mm	mm	\N	\N	\N	\N
5	Zentimeter	cm	cm	\N	\N	\N	\N
6	Meter	m	m	\N	\N	\N	\N
7	Kilometer	km	km	\N	\N	\N	\N
8	Bar	 b	b	\N	\N	\N	\N
9	Quadratmeter	m²	m2	\N	\N	\N	\N
10	Hektar	ha	ha	\N	\N	\N	\N
11	Kelvin	K	K	\N	\N	\N	\N
12	Kilogramm	kg	kg	\N	\N	\N	\N
13	Gramm	g	g	\N	\N	\N	\N
14	Pascal	Pa	Pa	\N	\N	\N	\N
15	Sekunde	sec	s	\N	\N	\N	\N
16	Minute	min	m	\N	\N	\N	\N
17	Stunde	hr	h	\N	\N	\N	\N
18	Tag	D	D	\N	\N	\N	\N
19	Ampere	A	A	\N	\N	\N	\N
20	Candela	cd	cd	\N	\N	\N	\N
22	Mol	mol	mol	\N	\N	\N	\N
23	Kilopascal	kPa	kPa	\N	\N	\N	\N
24	Dimensionslos	-	-	\N	\N	\N	\N
26	Grad	deg.	deg.	\N	\N	\N	\N
27	Zentisiemens pro Meter	cs/m	cs/m	\N	\N	\N	\N
28	Watt pro Quadratmeter	W/m²	W/m2	\N	\N	\N	\N
29	Geschwindigkeit	m/s	m/s	\N	\N	\N	\N
\.


--
-- Name: lt_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_unit_id_seq', 1, false);


--
-- Data for Name: lt_user; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY lt_user (id, is_institution, first_name, last_name, institution_name, department, email, comment, created_on, updated_on) FROM stdin;
\.


--
-- Name: lt_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('lt_user_id_seq', 1, false);


--
-- Data for Name: nm_meta_domain; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY nm_meta_domain (meta_id, domain_id) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY spatial_ref_sys  FROM stdin;
\.


--
-- Data for Name: tbl_data; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY tbl_data (tstamp, meta_id, value) FROM stdin;
\.


--
-- Data for Name: tbl_data_source; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY tbl_data_source (id, source_type_id, source_path, settings, created_on, updated_on) FROM stdin;
1	1	tbl_data	\N	\N	\N
\.


--
-- Name: tbl_data_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('tbl_data_source_id_seq', 1, false);


--
-- Data for Name: tbl_meta; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY tbl_meta (id, ts_start, ts_stop, external_id, support, spacing, creator_id, publisher_id, geometry_id, license_id, quality_id, site_id, soil_id, variable_id, sensor_id, source_id, comment, created_on, updated_on) FROM stdin;
\.


--
-- Name: tbl_meta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('tbl_meta_id_seq', 1, false);


--
-- Data for Name: tbl_sensor; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY tbl_sensor (id, sensor_name, manufacturer, documentation_url, last_configured, valid_until, sensor_comment, created_on, updated_on) FROM stdin;
\.


--
-- Name: tbl_sensor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('tbl_sensor_id_seq', 1, false);


--
-- Data for Name: tbl_variable; Type: TABLE DATA; Schema: public; Owner: "www-data"
--

COPY tbl_variable (id, variable_name, variable_abbrev, variable_symbol, unit_id, created_on, updated_on) FROM stdin;
1	Lufttemperatur	T	T	1	\N	\N
2	relative Luftfeuchte	rel. rH	rH	2	\N	\N
3	Luftdruck	p	p	3	\N	\N
4	Niederschlag	R	R	4	\N	\N
5	Geländehöhe	H.ü. NN	H	6	\N	\N
6	volumetrischer Wassergehalt	Theta	Th	2	\N	\N
7	gravimetrischer Wassergehalt 	w	w	2	\N	\N
8	Sättigungsgrad	Sw	Sw	24	\N	\N
9	Windrichtung	D	D	26	\N	\N
10	elektrische Leitfähigkeit	sigma	s	27	\N	\N
12	Bodentemperatur	T	T	1	\N	\N
13	Matrixpotential	Psi	P	23	\N	\N
14	Wasserstand	H	H	6	\N	\N
15	spezifische Leitfähigkeit	sigma	s	27	\N	\N
16	Wassertemperatur	T	T	1	\N	\N
17	Nettostrahlung	R	R	28	\N	\N
18	Windgeschwindigkeit	w	w	29	\N	\N
19	Sap Flow	SV	SV	29	\N	\N
\.


--
-- Name: tbl_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: "www-data"
--

SELECT pg_catalog.setval('tbl_variable_id_seq', 1, false);


--
-- Name: lt_domain_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_domain
    ADD CONSTRAINT lt_domain_pkey PRIMARY KEY (id);


--
-- Name: lt_license_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_license
    ADD CONSTRAINT lt_license_pkey PRIMARY KEY (id);


--
-- Name: lt_location_geom_key; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_location
    ADD CONSTRAINT lt_location_geom_key UNIQUE (geom);


--
-- Name: lt_location_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_location
    ADD CONSTRAINT lt_location_pkey PRIMARY KEY (id);


--
-- Name: lt_project_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_project
    ADD CONSTRAINT lt_project_pkey PRIMARY KEY (id);


--
-- Name: lt_quality_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_quality
    ADD CONSTRAINT lt_quality_pkey PRIMARY KEY (id);


--
-- Name: lt_site_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_site
    ADD CONSTRAINT lt_site_pkey PRIMARY KEY (id);


--
-- Name: lt_soil_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_soil
    ADD CONSTRAINT lt_soil_pkey PRIMARY KEY (id);


--
-- Name: lt_source_type_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_source_type
    ADD CONSTRAINT lt_source_type_pkey PRIMARY KEY (id);


--
-- Name: lt_source_type_type_name_key; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_source_type
    ADD CONSTRAINT lt_source_type_type_name_key UNIQUE (type_name);


--
-- Name: lt_unit_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_unit
    ADD CONSTRAINT lt_unit_pkey PRIMARY KEY (id);


--
-- Name: lt_unit_unit_name_key; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_unit
    ADD CONSTRAINT lt_unit_unit_name_key UNIQUE (unit_name);


--
-- Name: lt_user_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_user
    ADD CONSTRAINT lt_user_pkey PRIMARY KEY (id);


--
-- Name: tbl_data_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_data
    ADD CONSTRAINT tbl_data_pkey PRIMARY KEY (tstamp, meta_id);


--
-- Name: tbl_data_source_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_data_source
    ADD CONSTRAINT tbl_data_source_pkey PRIMARY KEY (id);


--
-- Name: tbl_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_pkey PRIMARY KEY (id);


--
-- Name: tbl_sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_sensor
    ADD CONSTRAINT tbl_sensor_pkey PRIMARY KEY (id);


--
-- Name: tbl_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_variable
    ADD CONSTRAINT tbl_variable_pkey PRIMARY KEY (id);


--
-- Name: tbl_variable_variable_name_key; Type: CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_variable
    ADD CONSTRAINT tbl_variable_variable_name_key UNIQUE (variable_name);


--
-- Name: idx_lt_location_geom; Type: INDEX; Schema: public; Owner: "www-data"
--

CREATE INDEX idx_lt_location_geom ON lt_location USING gist (geom);


--
-- Name: ix_lt_project_project_name; Type: INDEX; Schema: public; Owner: "www-data"
--

CREATE UNIQUE INDEX ix_lt_project_project_name ON lt_project USING btree (project_name);


--
-- Name: lt_domain_pid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_domain
    ADD CONSTRAINT lt_domain_pid_fkey FOREIGN KEY (pid) REFERENCES lt_domain(id);


--
-- Name: lt_domain_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_domain
    ADD CONSTRAINT lt_domain_project_id_fkey FOREIGN KEY (project_id) REFERENCES lt_project(id);


--
-- Name: lt_location_srid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_location
    ADD CONSTRAINT lt_location_srid_fkey FOREIGN KEY (srid) REFERENCES spatial_ref_sys(srid);


--
-- Name: lt_project_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY lt_project
    ADD CONSTRAINT lt_project_user_id_fkey FOREIGN KEY (user_id) REFERENCES lt_user(id);


--
-- Name: nm_meta_domain_domain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY nm_meta_domain
    ADD CONSTRAINT nm_meta_domain_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES lt_domain(id);


--
-- Name: nm_meta_domain_meta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY nm_meta_domain
    ADD CONSTRAINT nm_meta_domain_meta_id_fkey FOREIGN KEY (meta_id) REFERENCES tbl_meta(id);


--
-- Name: tbl_data_meta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_data
    ADD CONSTRAINT tbl_data_meta_id_fkey FOREIGN KEY (meta_id) REFERENCES tbl_meta(id);


--
-- Name: tbl_data_source_source_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_data_source
    ADD CONSTRAINT tbl_data_source_source_type_id_fkey FOREIGN KEY (source_type_id) REFERENCES lt_source_type(id);


--
-- Name: tbl_meta_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES lt_user(id);


--
-- Name: tbl_meta_geometry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_geometry_id_fkey FOREIGN KEY (geometry_id) REFERENCES lt_location(id);


--
-- Name: tbl_meta_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_license_id_fkey FOREIGN KEY (license_id) REFERENCES lt_license(id);


--
-- Name: tbl_meta_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES lt_user(id);


--
-- Name: tbl_meta_quality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_quality_id_fkey FOREIGN KEY (quality_id) REFERENCES lt_quality(id);


--
-- Name: tbl_meta_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES tbl_sensor(id);


--
-- Name: tbl_meta_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_site_id_fkey FOREIGN KEY (site_id) REFERENCES lt_site(id);


--
-- Name: tbl_meta_soil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_soil_id_fkey FOREIGN KEY (soil_id) REFERENCES lt_soil(id);


--
-- Name: tbl_meta_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_source_id_fkey FOREIGN KEY (source_id) REFERENCES tbl_data_source(id);


--
-- Name: tbl_meta_variable_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_meta
    ADD CONSTRAINT tbl_meta_variable_id_fkey FOREIGN KEY (variable_id) REFERENCES tbl_variable(id);


--
-- Name: tbl_variable_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: "www-data"
--

ALTER TABLE ONLY tbl_variable
    ADD CONSTRAINT tbl_variable_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES lt_unit(id);


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

