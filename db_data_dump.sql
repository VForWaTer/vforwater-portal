--
-- PostgreSQL database dump
--

-- Dumped from database version 10.13
-- Dumped by pg_dump version 10.13

-- Started on 2021-02-09 08:26:53 CET

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

--
-- TOC entry 5686 (class 0 OID 87441)
-- Dependencies: 236
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.alembic_version (version_num) FROM stdin;
1aade7b95b90
\.


--
-- TOC entry 5715 (class 0 OID 134101)
-- Dependencies: 275
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 5711 (class 0 OID 134055)
-- Dependencies: 271
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	vfw_home	datasources
2	vfw_home	datasourcetypes
3	vfw_home	datatypes
4	vfw_home	details
5	vfw_home	entries
6	vfw_home	entrygroups
7	vfw_home	entrygrouptypes
8	vfw_home	keywords
9	vfw_home	licenses
10	vfw_home	locationfilter
11	vfw_home	logs
12	vfw_home	personroles
13	vfw_home	persons
14	vfw_home	spatialscales
15	vfw_home	temporalscales
16	vfw_home	thesaurus
17	vfw_home	units
18	vfw_home	variables
19	vfw_home	generic1ddata
20	vfw_home	generic2ddata
21	vfw_home	genericgeometrydata
22	vfw_home	geomtimeseries
23	vfw_home	nmentrygroups
24	vfw_home	nmkeywordsentries
25	vfw_home	nmpersonsentries
26	vfw_home	timeseries
27	vfw_home	timeseries2d
28	admin	logentry
29	auth	permission
30	auth	group
31	auth	user
32	contenttypes	contenttype
33	sessions	session
34	wps_gui	webprocessingservice
35	wps_gui	wpsresults
36	upload	uploadedfile
37	author_manage	customuser
38	author_manage	profile
39	author_manage	maintainer
40	author_manage	resource
41	author_manage	deletionrequest
42	author_manage	accessrequest
43	author_manage	owner
\.


--
-- TOC entry 5713 (class 0 OID 134093)
-- Dependencies: 273
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add datasources	1	add_datasources
2	Can change datasources	1	change_datasources
3	Can delete datasources	1	delete_datasources
4	Can view datasources	1	view_datasources
5	Can add datasource types	2	add_datasourcetypes
6	Can change datasource types	2	change_datasourcetypes
7	Can delete datasource types	2	delete_datasourcetypes
8	Can view datasource types	2	view_datasourcetypes
9	Can add datatypes	3	add_datatypes
10	Can change datatypes	3	change_datatypes
11	Can delete datatypes	3	delete_datatypes
12	Can view datatypes	3	view_datatypes
13	Can add details	4	add_details
14	Can change details	4	change_details
15	Can delete details	4	delete_details
16	Can view details	4	view_details
17	Can add entries	5	add_entries
18	Can change entries	5	change_entries
19	Can delete entries	5	delete_entries
20	Can view entries	5	view_entries
21	Can add entrygroups	6	add_entrygroups
22	Can change entrygroups	6	change_entrygroups
23	Can delete entrygroups	6	delete_entrygroups
24	Can view entrygroups	6	view_entrygroups
25	Can add entrygroup types	7	add_entrygrouptypes
26	Can change entrygroup types	7	change_entrygrouptypes
27	Can delete entrygroup types	7	delete_entrygrouptypes
28	Can view entrygroup types	7	view_entrygrouptypes
29	Can add keywords	8	add_keywords
30	Can change keywords	8	change_keywords
31	Can delete keywords	8	delete_keywords
32	Can view keywords	8	view_keywords
33	Can add licenses	9	add_licenses
34	Can change licenses	9	change_licenses
35	Can delete licenses	9	delete_licenses
36	Can view licenses	9	view_licenses
37	Can add location filter	10	add_locationfilter
38	Can change location filter	10	change_locationfilter
39	Can delete location filter	10	delete_locationfilter
40	Can view location filter	10	view_locationfilter
41	Can add logs	11	add_logs
42	Can change logs	11	change_logs
43	Can delete logs	11	delete_logs
44	Can view logs	11	view_logs
45	Can add person roles	12	add_personroles
46	Can change person roles	12	change_personroles
47	Can delete person roles	12	delete_personroles
48	Can view person roles	12	view_personroles
49	Can add persons	13	add_persons
50	Can change persons	13	change_persons
51	Can delete persons	13	delete_persons
52	Can view persons	13	view_persons
53	Can add spatial scales	14	add_spatialscales
54	Can change spatial scales	14	change_spatialscales
55	Can delete spatial scales	14	delete_spatialscales
56	Can view spatial scales	14	view_spatialscales
57	Can add temporal scales	15	add_temporalscales
58	Can change temporal scales	15	change_temporalscales
59	Can delete temporal scales	15	delete_temporalscales
60	Can view temporal scales	15	view_temporalscales
61	Can add thesaurus	16	add_thesaurus
62	Can change thesaurus	16	change_thesaurus
63	Can delete thesaurus	16	delete_thesaurus
64	Can view thesaurus	16	view_thesaurus
65	Can add units	17	add_units
66	Can change units	17	change_units
67	Can delete units	17	delete_units
68	Can view units	17	view_units
69	Can add variables	18	add_variables
70	Can change variables	18	change_variables
71	Can delete variables	18	delete_variables
72	Can view variables	18	view_variables
73	Can add generic1d data	19	add_generic1ddata
74	Can change generic1d data	19	change_generic1ddata
75	Can delete generic1d data	19	delete_generic1ddata
76	Can view generic1d data	19	view_generic1ddata
77	Can add generic2d data	20	add_generic2ddata
78	Can change generic2d data	20	change_generic2ddata
79	Can delete generic2d data	20	delete_generic2ddata
80	Can view generic2d data	20	view_generic2ddata
81	Can add generic geometry data	21	add_genericgeometrydata
82	Can change generic geometry data	21	change_genericgeometrydata
83	Can delete generic geometry data	21	delete_genericgeometrydata
84	Can view generic geometry data	21	view_genericgeometrydata
85	Can add geom timeseries	22	add_geomtimeseries
86	Can change geom timeseries	22	change_geomtimeseries
87	Can delete geom timeseries	22	delete_geomtimeseries
88	Can view geom timeseries	22	view_geomtimeseries
89	Can add nm entrygroups	23	add_nmentrygroups
90	Can change nm entrygroups	23	change_nmentrygroups
91	Can delete nm entrygroups	23	delete_nmentrygroups
92	Can view nm entrygroups	23	view_nmentrygroups
93	Can add nm keywords entries	24	add_nmkeywordsentries
94	Can change nm keywords entries	24	change_nmkeywordsentries
95	Can delete nm keywords entries	24	delete_nmkeywordsentries
96	Can view nm keywords entries	24	view_nmkeywordsentries
97	Can add nm persons entries	25	add_nmpersonsentries
98	Can change nm persons entries	25	change_nmpersonsentries
99	Can delete nm persons entries	25	delete_nmpersonsentries
100	Can view nm persons entries	25	view_nmpersonsentries
101	Can add timeseries	26	add_timeseries
102	Can change timeseries	26	change_timeseries
103	Can delete timeseries	26	delete_timeseries
104	Can view timeseries	26	view_timeseries
105	Can add timeseries2d	27	add_timeseries2d
106	Can change timeseries2d	27	change_timeseries2d
107	Can delete timeseries2d	27	delete_timeseries2d
108	Can view timeseries2d	27	view_timeseries2d
109	Can add log entry	28	add_logentry
110	Can change log entry	28	change_logentry
111	Can delete log entry	28	delete_logentry
112	Can view log entry	28	view_logentry
113	Can add permission	29	add_permission
114	Can change permission	29	change_permission
115	Can delete permission	29	delete_permission
116	Can view permission	29	view_permission
117	Can add group	30	add_group
118	Can change group	30	change_group
119	Can delete group	30	delete_group
120	Can view group	30	view_group
121	Can add user	31	add_user
122	Can change user	31	change_user
123	Can delete user	31	delete_user
124	Can view user	31	view_user
125	Can add content type	32	add_contenttype
126	Can change content type	32	change_contenttype
127	Can delete content type	32	delete_contenttype
128	Can view content type	32	view_contenttype
129	Can add session	33	add_session
130	Can change session	33	change_session
131	Can delete session	33	delete_session
132	Can view session	33	view_session
133	Can add Web Processing Service	34	add_webprocessingservice
134	Can change Web Processing Service	34	change_webprocessingservice
135	Can delete Web Processing Service	34	delete_webprocessingservice
136	Can view Web Processing Service	34	view_webprocessingservice
137	Can add wps results	35	add_wpsresults
138	Can change wps results	35	change_wpsresults
139	Can delete wps results	35	delete_wpsresults
140	Can view wps results	35	view_wpsresults
141	Can add uploaded file	36	add_uploadedfile
142	Can change uploaded file	36	change_uploadedfile
143	Can delete uploaded file	36	delete_uploadedfile
144	Can view uploaded file	36	view_uploadedfile
145	Can add custom user	37	add_customuser
146	Can change custom user	37	change_customuser
147	Can delete custom user	37	delete_customuser
148	Can view custom user	37	view_customuser
149	Can add profile	38	add_profile
150	Can change profile	38	change_profile
151	Can delete profile	38	delete_profile
152	Can view profile	38	view_profile
153	Can add maintainer	39	add_maintainer
154	Can change maintainer	39	change_maintainer
155	Can delete maintainer	39	delete_maintainer
156	Can view maintainer	39	view_maintainer
157	Can add resource	40	add_resource
158	Can change resource	40	change_resource
159	Can delete resource	40	delete_resource
160	Can view resource	40	view_resource
161	Can add deletion request	41	add_deletionrequest
162	Can change deletion request	41	change_deletionrequest
163	Can delete deletion request	41	delete_deletionrequest
164	Can view deletion request	41	view_deletionrequest
165	Can add access request	42	add_accessrequest
166	Can change access request	42	change_accessrequest
167	Can delete access request	42	delete_accessrequest
168	Can view access request	42	view_accessrequest
169	Can add owner	43	add_owner
170	Can change owner	43	change_owner
171	Can delete owner	43	delete_owner
172	Can view owner	43	view_owner
\.


--
-- TOC entry 5717 (class 0 OID 134111)
-- Dependencies: 277
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5719 (class 0 OID 134119)
-- Dependencies: 279
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$150000$53rMLU46qejd$Bu0AD+sfx5dzkOR37REDtOl2qdGu0Nlfc66Mryng+0k=	2019-10-16 10:35:42.389063+02	f	eric			eric@uni.de	f	t	2019-09-27 14:11:02+02
2	pbkdf2_sha256$150000$9yzIT4QTiciu$TI6DhRboZIy03WPiwqsk7JClOsNHXe5tdsYBuzQuVdg=	2020-02-20 11:00:35.792647+01	t	frank			fra@blu.edu	t	t	2020-02-18 14:15:04.160661+01
5	pbkdf2_sha256$150000$lZiILV9BZdIe$nAi9uCnJL7BT+cvSnQcssUlGj0b67PXiYPWUZNqGAD0=	2020-10-06 10:17:16.552605+02	t	christin	Chris	Tine	christi@ti.ch	t	t	2019-09-27 14:13:13+02
\.


--
-- TOC entry 5721 (class 0 OID 134129)
-- Dependencies: 281
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 5723 (class 0 OID 134137)
-- Dependencies: 283
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 5666 (class 0 OID 87177)
-- Dependencies: 216
-- Data for Name: datasource_types; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.datasource_types (id, name, title, description) FROM stdin;
1	internal	Internal Table	Table inside the same database instance.
2	external	External Table	SQL table in an external database instance, but of same structure.
3	csv	Local CSV File	Standard csv file source on the database server machine
\.


--
-- TOC entry 5690 (class 0 OID 87468)
-- Dependencies: 240
-- Data for Name: datatypes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.datatypes (id, parent_id, name, title, description) FROM stdin;
1	\N	blob	File Blob	Any kind of file-like-structure. Reader will only return file paths. Not for use in production. Can be used as a placeholder for custom data management.
11	\N	array	generic array structure	Arrays are a series of data objects, without index.
12	11	iarray	indexed array	Array with additional index information for each element, that is not a datetime.
13	12	varray	named, indexed array	An iarray that additionally has a name property of any valid metacatalog Variable.
14	11	timeseries	timeseries	Array indexed by datetime information. The datetimes need to be of increasing order.
15	14	vtimeseries	named timeseries	Timeseries that holds an additional Variable name to describe the content.
16	\N	ndarray	generic mulidimensional array	NDArrays are multidimensional arrays of common atomic data-type.
17	16	raster	Raster data	GDAL conform raster images.
18	17	vraster	named raster data	The named raster images are not implemented yet.
19	16	2darray	2D-array	Special case of NDArray with exactly two dimensions.
20	16	idataframe	indexed table	NDArray with any index except datetime information.
21	20	vdataframe	named, indexed table	idataframe with additional name property of any valid metacatalog Variable.
22	16	time-dataframe	timeseries table	NDArray indexed by datetime information. The datetimes need to be of increasing order.
23	22	vtime-dataframe	named timeseries table	Timeseries table that holds an additional Variable name to describe the content.
\.


--
-- TOC entry 5694 (class 0 OID 87501)
-- Dependencies: 244
-- Data for Name: spatial_scales; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.spatial_scales (id, resolution, extent, support) FROM stdin;
\.


--
-- TOC entry 5692 (class 0 OID 87489)
-- Dependencies: 242
-- Data for Name: temporal_scales; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.temporal_scales (id, resolution, observation_start, observation_end, support) FROM stdin;
1	P0DT0H10M0S	2015-04-23 08:00:00	2015-11-03 12:00:00	1.0
2	P0DT0H10M0S	2015-05-07 15:40:00	2015-08-30 10:40:00	1.0
3	P0DT0H10M0S	2015-04-22 20:10:00	2015-11-03 12:00:00	1.0
4	P0DT0H10M0S	2015-04-23 10:20:00	2015-11-03 13:50:00	1.0
5	P0DT0H10M0S	2015-04-23 10:20:00	2015-08-19 10:40:00	1.0
6	P0DT0H10M0S	2015-04-22 18:00:00	2015-10-11 17:30:00	1.0
7	P0DT0H10M0S	2015-04-22 22:00:00	2015-11-03 13:50:00	1.0
8	P0DT0H10M0S	2015-04-22 22:10:00	2015-10-20 22:20:00	1.0
9	P0DT0H10M0S	2015-04-23 20:00:00	2015-10-12 08:10:00	1.0
10	P0DT0H10M0S	2015-04-23 12:20:00	2015-11-05 11:50:00	1.0
11	P0DT0H10M0S	2015-04-23 12:20:00	2015-11-05 11:50:00	1.0
12	P0DT0H10M0S	2015-05-03 00:20:00	2015-11-05 11:50:00	1.0
13	P0DT0H10M0S	2015-04-23 14:50:00	2015-11-05 11:50:00	1.0
14	P0DT0H10M0S	2015-04-23 23:40:00	2015-10-26 21:00:00	1.0
15	P0DT0H10M0S	2015-04-23 08:00:00	2015-10-08 07:10:00	1.0
16	P0DT0H10M0S	2015-04-23 08:00:00	2015-10-12 06:50:00	1.0
17	P0DT0H10M0S	2015-04-23 12:30:00	2015-11-05 11:50:00	1.0
\.


--
-- TOC entry 5672 (class 0 OID 87222)
-- Dependencies: 222
-- Data for Name: datasources; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.datasources (id, type_id, path, args, creation, "lastUpdate", encoding, datatype_id, temporal_scale_id, spatial_scale_id) FROM stdin;
18	1	timeseries	{}	2020-11-02 12:25:03.073151	2020-11-02 12:25:03.073162	utf-8	14	\N	\N
19	1	timeseries	{}	2020-11-02 12:25:03.201276	2020-11-02 12:25:03.201285	utf-8	14	\N	\N
1	1	timeseries	{}	\N	2020-07-20 07:51:41.541631	utf-8	14	1	\N
2	1	timeseries	{}	\N	2020-07-20 07:51:41.691972	utf-8	14	2	\N
3	1	timeseries	{}	\N	2020-07-20 07:51:41.853243	utf-8	14	3	\N
4	1	timeseries	{}	\N	2020-07-20 07:51:42.018608	utf-8	14	4	\N
5	1	timeseries	{}	\N	2020-07-20 07:51:42.134406	utf-8	14	5	\N
6	1	timeseries	{}	\N	2020-07-20 07:51:42.271609	utf-8	14	6	\N
7	1	timeseries	{}	\N	2020-07-20 07:51:42.448146	utf-8	14	7	\N
8	1	timeseries	{}	\N	2020-07-20 07:51:42.605308	utf-8	14	8	\N
9	1	timeseries	{}	\N	2020-07-20 07:51:42.762138	utf-8	14	9	\N
10	1	timeseries	{}	\N	2020-07-20 07:51:42.933666	utf-8	14	10	\N
11	1	timeseries	{}	\N	2020-07-20 07:51:43.1099	utf-8	14	11	\N
12	1	timeseries	{}	\N	2020-07-20 07:51:43.275066	utf-8	14	12	\N
13	1	timeseries	{}	\N	2020-07-20 07:51:43.44661	utf-8	14	13	\N
14	1	timeseries	{}	\N	2020-07-20 07:51:43.605403	utf-8	14	14	\N
15	1	timeseries	{}	\N	2020-07-20 07:51:43.760654	utf-8	14	15	\N
16	1	timeseries	{}	\N	2020-07-20 07:51:43.910397	utf-8	14	16	\N
17	1	timeseries	{}	\N	2020-07-20 07:51:44.091978	utf-8	14	17	\N
\.


--
-- TOC entry 5688 (class 0 OID 87448)
-- Dependencies: 238
-- Data for Name: thesaurus; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.thesaurus (id, uuid, name, title, organisation, description, url) FROM stdin;
1	2e54668d-8fae-429f-a511-efe529420b12	GCMD	NASA/GCMD Earth Science Keywords	NASA	NASA Global Clime change Master Dictionary Science Keywords	https://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/sciencekeywords/?format=xml
\.


--
-- TOC entry 5656 (class 0 OID 87115)
-- Dependencies: 206
-- Data for Name: keywords; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.keywords (id, parent_id, value, uuid, full_path, thesaurus_id) FROM stdin;
21	2	PALEOCLIMATE	c7245882-84a1-4192-acfa-a758b5b9c151	EARTH SCIENCE > PALEOCLIMATE	1
22	2	SOLID EARTH	2b9ad978-d986-4d63-b477-0f5efc8ace72	EARTH SCIENCE > SOLID EARTH	1
173	20	OCEAN OPTICS	457883c4-b30c-4d26-bed8-6c2887ebbc90	EARTH SCIENCE > OCEANS > OCEAN OPTICS	1
174	20	OCEAN PRESSURE	bfa56100-6fb5-4e49-9633-298fa3b45508	EARTH SCIENCE > OCEANS > OCEAN PRESSURE	1
5728	158	SOIL PH	357193c5-154d-487b-a1c3-a1a90d15918c	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL PH	1
17	2	CRYOSPHERE	fa0a36c3-2503-4662-98cd-7f3e74ce9f80	EARTH SCIENCE > CRYOSPHERE	1
18	2	HUMAN DIMENSIONS	fb93d937-c17c-45d0-a9e3-ca5c8a800ca8	EARTH SCIENCE > HUMAN DIMENSIONS	1
19	2	LAND SURFACE	6a426480-c58f-4b6b-8e35-0975b7f6edb5	EARTH SCIENCE > LAND SURFACE	1
20	2	OCEANS	91697b7d-8f2b-4954-850e-61d5f61c867d	EARTH SCIENCE > OCEANS	1
1	\N	EARTH SCIENCE SERVICES	894f9116-ae3c-40b6-981d-5113de961710	EARTH SCIENCE SERVICES	1
2	\N	EARTH SCIENCE	e9f67a66-e9fc-435c-b720-ae32a2c3d8f5	EARTH SCIENCE	1
3	1	DATA ANALYSIS AND VISUALIZATION	41adc080-c182-4753-9666-435f8b1c913f	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION	1
4	1	DATA MANAGEMENT/DATA HANDLING	02d92216-70c6-437c-8c15-2b76f2132921	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING	1
5	1	EDUCATION/OUTREACH	dc2088f9-ffb7-41c3-b0a1-856ecfec89de	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH	1
6	1	ENVIRONMENTAL ADVISORIES	09d00879-6d96-4df4-9f50-73bd761118d9	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES	1
7	1	HAZARDS MANAGEMENT	464de0a5-2bb9-4172-9fd3-1634cbc4e739	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT	1
8	1	METADATA HANDLING	a1fedfa9-569f-4313-8ce1-db95513c5469	EARTH SCIENCE SERVICES > METADATA HANDLING	1
9	1	MODELS	e1f20631-b5b9-438c-b5c2-b1fa0fce100a	EARTH SCIENCE SERVICES > MODELS	1
10	1	REFERENCE AND INFORMATION SERVICES	a3a5d0dd-0e8f-4649-8a55-25f9251e1008	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES	1
11	1	WEB SERVICES	1d550f3a-1c8c-4ef5-beff-74cfe7794f12	EARTH SCIENCE SERVICES > WEB SERVICES	1
12	2	AGRICULTURE	a956d045-3b12-441c-8a18-fac7d33b2b4e	EARTH SCIENCE > AGRICULTURE	1
13	2	ATMOSPHERE	c47f6052-634e-40ef-a5ac-13f69f6f4c2a	EARTH SCIENCE > ATMOSPHERE	1
14	2	BIOLOGICAL CLASSIFICATION	fbec5145-79e6-4ed0-a804-6228aa6daba5	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION	1
15	2	BIOSPHERE	91c64c46-d040-4daa-b26c-61952fdfaf50	EARTH SCIENCE > BIOSPHERE	1
16	2	CLIMATE INDICATORS	23703b6b-ee15-4512-b5b2-f441547e2edf	EARTH SCIENCE > CLIMATE INDICATORS	1
23	2	SPECTRAL/ENGINEERING	83150c54-5da8-4ee8-9579-19b95a8dc10c	EARTH SCIENCE > SPECTRAL/ENGINEERING	1
24	2	SUN-EARTH INTERACTIONS	57383ac5-614c-4b84-9202-e137b000422b	EARTH SCIENCE > SUN-EARTH INTERACTIONS	1
25	2	TERRESTRIAL HYDROSPHERE	885735f3-121e-4ca0-ac8b-f37dbc972f03	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE	1
26	3	CALIBRATION/VALIDATION	4f938731-d686-4d89-b72b-ff60474bb1f0	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > CALIBRATION/VALIDATION	1
27	3	GEOGRAPHIC INFORMATION SYSTEMS	794e3c3b-791f-44de-9ff3-358d8ed74733	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > GEOGRAPHIC INFORMATION SYSTEMS	1
28	3	GLOBAL POSITIONING SYSTEMS	f082ad51-4ce4-4ffe-be50-6753c4f997ae	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > GLOBAL POSITIONING SYSTEMS	1
29	3	STATISTICAL APPLICATIONS	997dc5a6-d83f-4d59-8c5a-1d901b069830	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > STATISTICAL APPLICATIONS	1
30	3	VISUALIZATION/IMAGE PROCESSING	4698858b-bf39-4a2c-9713-e41757739eff	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > VISUALIZATION/IMAGE PROCESSING	1
31	4	ARCHIVING	c75db4f8-716c-47a8-a2f4-34e5a48296b0	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > ARCHIVING	1
32	4	CATALOGING	434d40e2-4e0b-408a-9811-ff878f4f0fb0	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > CATALOGING	1
33	4	DATA COMPRESSION	e0d7fb1f-5233-4664-8e83-3c65ca344f41	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA COMPRESSION	1
34	4	DATA DELIVERY	9916f643-05b4-4f0e-91e0-59922c6e09fc	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA DELIVERY	1
35	4	DATA INTEROPERABILITY	0f3573bc-3cb7-4cec-a5bb-1bb6b7ab9057	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA INTEROPERABILITY	1
36	4	DATA MINING	07291e32-fd39-45e8-a603-7443cb780976	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA MINING	1
37	4	DATA NETWORKING/DATA TRANSFER TOOLS	80e34388-3d24-4ff9-8d23-784fad52c432	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA NETWORKING/DATA TRANSFER TOOLS	1
38	4	DATA SEARCH AND RETRIEVAL	86cbb2d3-6783-4d9b-9dc1-b0aea78f98ea	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA SEARCH AND RETRIEVAL	1
39	4	MEDIA TRANSFER/DATA RESCUE	fc757c55-83b4-400e-9d23-25bcad230603	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > MEDIA TRANSFER/DATA RESCUE	1
40	4	SUBSETTING/SUPERSETTING	cc9e67fc-eafa-43cc-879f-0cb56b25bc39	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > SUBSETTING/SUPERSETTING	1
41	4	TRANSFORMATION/CONVERSION	31ab3c10-1f10-4372-82d4-4c0c4be5999f	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > TRANSFORMATION/CONVERSION	1
42	5	CURRICULUM SUPPORT	97675827-9b0a-4d13-a795-d4a3e78c476a	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > CURRICULUM SUPPORT	1
43	5	EXHIBIT MATERIALS	9f8a6a52-df35-487d-9a74-74b76943e0c0	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > EXHIBIT MATERIALS	1
44	5	INTERACTIVE PROGRAMS	247b151a-2f56-41f9-8a19-51e34a64d61e	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > INTERACTIVE PROGRAMS	1
45	6	AGRICULTURAL ADVISORIES	a9394dee-8c4e-47a8-b630-6549ac1cb717	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > AGRICULTURAL ADVISORIES	1
46	6	FIRE ADVISORIES	7f71a0a0-3da7-42b9-b134-c0a824dff971	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > FIRE ADVISORIES	1
47	6	GEOLOGICAL ADVISORIES	13b8bcd4-7566-49e5-9975-ea15470474ab	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > GEOLOGICAL ADVISORIES	1
48	6	HEALTH ADVISORIES	370eba54-962b-4e59-9686-86d5c5ab9c88	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HEALTH ADVISORIES	1
49	6	HYDROLOGICAL ADVISORIES	7406a787-6ab6-429f-bc09-9a86d393e114	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HYDROLOGICAL ADVISORIES	1
50	6	MARINE ADVISORIES	39f5a91f-c5b6-4aa9-a0c6-05530306f17b	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES	1
51	6	SPACE WEATHER ADVISORIES	09d1435d-99de-4149-ba64-d98c3335a383	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES	1
52	6	WEATHER/CLIMATE ADVISORIES	89554e78-d69d-4a38-b7f1-78d9e1e4aa57	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES	1
101	12	FOREST SCIENCE	22ec2f9b-1f1a-469b-bc09-851d58637ff4	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE	1
53	7	DISASTER RECOVERY/RELIEF	6b2fad63-2230-4d54-8f31-fee604d1f977	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > DISASTER RECOVERY/RELIEF	1
54	7	DISASTER RESPONSE	d7aa220d-4012-4ab1-98c8-0cc4157a48f3	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > DISASTER RESPONSE	1
55	7	HAZARDS MAPPING	c9a13e09-98de-4ace-8d4c-b01aa04347f4	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING	1
56	7	HAZARDS MITIGATION	a2e9c7b9-96fd-449f-91db-7ab5e2dd679e	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MITIGATION	1
57	7	HAZARDS PLANNING	5c14b001-518f-460b-90fe-139bf192d1f2	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS PLANNING	1
58	8	AUTHORING TOOLS	5aad0680-cae2-402b-8311-3fb4ddc892bd	EARTH SCIENCE SERVICES > METADATA HANDLING > AUTHORING TOOLS	1
59	8	DATA DISCOVERY	90c21a67-6703-4b59-96ee-c2c602652c80	EARTH SCIENCE SERVICES > METADATA HANDLING > DATA DISCOVERY	1
60	8	METADATA TRANSFORMATION/CONVERSION	f29a3482-de42-4027-b5f4-87a3f7cd28af	EARTH SCIENCE SERVICES > METADATA HANDLING > METADATA TRANSFORMATION/CONVERSION	1
61	8	SERVICE DISCOVERY	f41dae97-a5ca-4c23-aec5-378448a14f92	EARTH SCIENCE SERVICES > METADATA HANDLING > SERVICE DISCOVERY	1
62	9	ANCILLARY MODELS	7872b9af-8c90-481e-aaa6-a47b736f0828	EARTH SCIENCE SERVICES > MODELS > ANCILLARY MODELS	1
63	9	ATMOSPHERIC CHEMISTRY MODELS	3668de06-8a7d-4667-beb8-d04dcac619b0	EARTH SCIENCE SERVICES > MODELS > ATMOSPHERIC CHEMISTRY MODELS	1
64	9	ATMOSPHERIC GENERAL CIRCULATION MODELS	063177a9-14cd-4750-9aa4-ad5d266bd7ad	EARTH SCIENCE SERVICES > MODELS > ATMOSPHERIC GENERAL CIRCULATION MODELS	1
65	9	CARBON CYCLE/CARBON BUDGET MODELS	640d703f-9312-4f11-8367-30a8bd8fc508	EARTH SCIENCE SERVICES > MODELS > CARBON CYCLE/CARBON BUDGET MODELS	1
66	9	CLIMATE CHANGE IMPACT ASSESSMENT MODELS	ea5ccefb-e390-43d5-8202-33e004565beb	EARTH SCIENCE SERVICES > MODELS > CLIMATE CHANGE IMPACT ASSESSMENT MODELS	1
67	9	COMPONENT PROCESS MODELS	f66e185f-7e17-4b5c-bc4e-523ddfbbe9ca	EARTH SCIENCE SERVICES > MODELS > COMPONENT PROCESS MODELS	1
68	9	COUPLED CLIMATE MODELS	c5b13fa4-0069-40ce-85cb-bfbab34c2058	EARTH SCIENCE SERVICES > MODELS > COUPLED CLIMATE MODELS	1
69	9	CRYOSPHERE MODELS	0a22b06c-eeed-46dc-b41b-af44ca94c419	EARTH SCIENCE SERVICES > MODELS > CRYOSPHERE MODELS	1
70	9	DIGITAL ELEVATION/DIGITAL TERRAIN MODELS	e5f94c93-e8af-4919-827f-9059dab9cf27	EARTH SCIENCE SERVICES > MODELS > DIGITAL ELEVATION/DIGITAL TERRAIN MODELS	1
71	9	DYNAMIC VEGETATION/ECOSYSTEM MODELS	adfee6d2-ca00-4f02-a570-5ccf0850cb55	EARTH SCIENCE SERVICES > MODELS > DYNAMIC VEGETATION/ECOSYSTEM MODELS	1
72	9	EARTH SCIENCE REANALYSES/ASSIMILATION MODELS	b8615aad-d2eb-45a3-98a7-4adac5bdf5a5	EARTH SCIENCE SERVICES > MODELS > EARTH SCIENCE REANALYSES/ASSIMILATION MODELS	1
73	9	GEOLOGIC/TECTONIC/PALEOCLIMATE MODELS	f96bf6c8-2f34-412a-b734-b2644f08a329	EARTH SCIENCE SERVICES > MODELS > GEOLOGIC/TECTONIC/PALEOCLIMATE MODELS	1
74	9	HYDROLOGIC AND TERRESTRIAL WATER CYCLE MODELS	2eb094d5-70bc-49fa-acb6-4ad07f4c7b08	EARTH SCIENCE SERVICES > MODELS > HYDROLOGIC AND TERRESTRIAL WATER CYCLE MODELS	1
75	9	LAND SURFACE MODELS	46461db7-88ba-446f-bdae-2d1e7f6302c2	EARTH SCIENCE SERVICES > MODELS > LAND SURFACE MODELS	1
76	9	OCEAN GENERAL CIRCULATION MODELS (OGCM)/REGIONAL OCEAN MODELS	c61a56a3-c08f-4989-92f3-0f0787688424	EARTH SCIENCE SERVICES > MODELS > OCEAN GENERAL CIRCULATION MODELS (OGCM)/REGIONAL OCEAN MODELS	1
77	9	PHENOMENOLOGICAL MODELS	93809fc5-da7c-4ca2-9585-70f09bd99898	EARTH SCIENCE SERVICES > MODELS > PHENOMENOLOGICAL MODELS	1
78	9	PHYSICAL/LABORATORY MODELS	1eb8b98b-73a1-4657-beda-76ab6355dd08	EARTH SCIENCE SERVICES > MODELS > PHYSICAL/LABORATORY MODELS	1
79	9	REGULATORY MODELS	e49f0aae-c2ef-4fd2-aaf4-ddfad074bb75	EARTH SCIENCE SERVICES > MODELS > REGULATORY MODELS	1
80	9	SOCIAL AND ECONOMIC MODELS	9a1dd3c3-a126-437e-ad04-9dc0a382d567	EARTH SCIENCE SERVICES > MODELS > SOCIAL AND ECONOMIC MODELS	1
81	9	SOLAR-ATMOSPHERE/SPACE-WEATHER MODELS	96400b5a-6932-41f2-a80c-5aba26a2b5de	EARTH SCIENCE SERVICES > MODELS > SOLAR-ATMOSPHERE/SPACE-WEATHER MODELS	1
82	9	WEATHER RESEARCH/FORECAST MODELS	92471848-b940-4b31-9165-f106457a4616	EARTH SCIENCE SERVICES > MODELS > WEATHER RESEARCH/FORECAST MODELS	1
83	10	BIBLIOGRAPHIC	80a8ca6d-8471-4d49-a99c-fa5954d93a55	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > BIBLIOGRAPHIC	1
84	10	DIGITAL/VIRTUAL REFERENCE DESKS	b37c3094-6ec8-4429-a80b-b332a7b4947d	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS	1
85	10	GAZETTEER	ac44c9c0-d0f1-4f25-b016-b57ca51d511e	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > GAZETTEER	1
86	10	IDENTIFICATION/CLASSIFICATION SYSTEMS	8f6ad4bb-ab00-4e5a-baee-2c17335ba809	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > IDENTIFICATION/CLASSIFICATION SYSTEMS	1
87	10	KNOWLEDGE/DECISION SYSTEMS	20ed3fa4-20fa-4531-8b02-dceda8eac81f	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > KNOWLEDGE/DECISION SYSTEMS	1
88	10	SUBSCRIPTION SERVICES	16d0abc3-8f75-4974-bdb4-df09a04bcfa3	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > SUBSCRIPTION SERVICES	1
89	10	THESAURI	52a71bf1-a099-4bb1-88c2-064203e3608c	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > THESAURI	1
90	11	DATA APPLICATION SERVICES	12a00b9e-52b3-44d0-bbfc-d8bb74173323	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES	1
91	11	DATA PROCESSING SERVICES	431eca76-9d34-4f86-b1d3-a0b40221e905	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES	1
92	11	INFORMATION MANAGEMENT SERVICES	46c929ad-8729-4484-8dc5-0a58a4e696a6	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES	1
93	12	AGRICULTURAL AQUATIC SCIENCES	ca227ff0-4742-4e51-a763-4582fa28291c	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL AQUATIC SCIENCES	1
94	12	AGRICULTURAL CHEMICALS	afd084b9-1f4c-4eb5-a58e-689a360e7abf	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL CHEMICALS	1
95	12	AGRICULTURAL ENGINEERING	b8018326-a186-4847-961d-8bd0727bbd5e	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL ENGINEERING	1
96	12	AGRICULTURAL PLANT SCIENCE	25be3b9a-9d4c-4b5b-8d24-b1f519913d90	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE	1
97	12	ANIMAL COMMODITIES	c9f1a861-2173-4124-962c-759f71b6f131	EARTH SCIENCE > AGRICULTURE > ANIMAL COMMODITIES	1
98	12	ANIMAL SCIENCE	b41894fa-2e3e-475b-b8f0-b6ffdd2d6e9c	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE	1
99	12	FEED PRODUCTS	c1f9f5fa-245c-4055-81cf-5230c076c0ce	EARTH SCIENCE > AGRICULTURE > FEED PRODUCTS	1
100	12	FOOD SCIENCE	b98f3a77-397d-41d7-9507-e7a3e47210b1	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE	1
102	12	PLANT COMMODITIES	d6560f20-3bef-41c6-8eec-9f913329b9ac	EARTH SCIENCE > AGRICULTURE > PLANT COMMODITIES	1
103	12	SOILS	199e3af8-4cf3-48ba-8b28-b9b54756b3db	EARTH SCIENCE > AGRICULTURE > SOILS	1
104	13	AEROSOLS	2e5a401b-1507-4f57-82b8-36557c13b154	EARTH SCIENCE > ATMOSPHERE > AEROSOLS	1
105	13	AIR QUALITY	77397026-09c9-44e0-b85f-77b2bc9b1630	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY	1
106	13	ALTITUDE	16bfcf54-f8e1-4c8e-9bd4-a1ac06ea95a0	EARTH SCIENCE > ATMOSPHERE > ALTITUDE	1
107	13	ATMOSPHERIC CHEMISTRY	b9c56939-c624-467d-b196-e56a5b660334	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY	1
108	13	ATMOSPHERIC ELECTRICITY	0af72e0e-52a5-4695-9eaf-d6fbb7991039	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC ELECTRICITY	1
109	13	ATMOSPHERIC PRESSURE	08fd82a1-4370-46a2-82ea-94c0f91498a7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE	1
110	13	ATMOSPHERIC RADIATION	4ad0c52d-6449-48ff-8678-adc6b2cebcb7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION	1
111	13	ATMOSPHERIC TEMPERATURE	35e1f93b-99b3-4430-b477-0ecafa80d67a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE	1
112	13	ATMOSPHERIC WATER VAPOR	286d2ae0-9d86-4ef0-a2b4-014843a98532	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR	1
113	13	ATMOSPHERIC WINDS	df160e31-ae45-41a4-9093-a80fe5303cea	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS	1
114	13	CLOUDS	162e2243-3266-4999-b352-d8a1a9dc82ac	EARTH SCIENCE > ATMOSPHERE > CLOUDS	1
115	13	PRECIPITATION	1532e590-a62d-46e3-8d03-2351bc48166a	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION	1
116	13	WEATHER EVENTS	b7d562cf-9b9b-4461-900b-50423a8c4d29	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS	1
117	14	ANIMALS/INVERTEBRATES	abc6f016-d1f0-4725-b847-639de054d13f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES	1
118	14	ANIMALS/VERTEBRATES	14802b53-b702-438f-8c8a-f51506807ce6	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES	1
119	14	BACTERIA/ARCHAEA	7437925f-7e10-4c96-af36-f3532ec24276	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > BACTERIA/ARCHAEA	1
120	14	FUNGI	3546cb0a-27a2-4914-85cf-1774b5c4ed19	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > FUNGI	1
121	14	PLANTS	0b4081fa-5233-4484-bc82-706976defa0e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS	1
122	14	PROTISTS	6a2a2417-1a9c-4767-bffd-6b99f9747bab	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS	1
123	14	VIRUSES	85510ccc-5dc9-44ff-871e-775e856714f8	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > VIRUSES	1
124	15	ECOLOGICAL DYNAMICS	6bef0291-a9ca-4832-bbb4-80459dc1493f	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS	1
125	15	ECOSYSTEMS	f1a25060-330c-4f84-9633-ed59ae8c64bf	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS	1
126	15	VEGETATION	c7b5c02c-724d-4a19-b824-98180f3900c9	EARTH SCIENCE > BIOSPHERE > VEGETATION	1
127	16	ATMOSPHERIC/OCEAN INDICATORS	5273c8c2-d30b-4666-b2d5-0388ce2741d0	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS	1
128	16	BIOSPHERIC INDICATORS	76943142-e5a9-4ecf-b496-050dd3d97101	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS	1
129	16	CLIMATE FEEDBACKS	de62c07e-96c6-44fb-a3a1-cd2902305691	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS	1
130	16	CRYOSPHERIC INDICATORS	76b8c21c-c221-4724-86ef-c07222cb152b	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS	1
131	16	ENVIRONMENTAL VULNERABILITY INDEX (EVI)	897b3d65-709c-4739-9ba6-85911295d843	EARTH SCIENCE > CLIMATE INDICATORS > ENVIRONMENTAL VULNERABILITY INDEX (EVI)	1
132	16	LAND SURFACE/AGRICULTURE INDICATORS	112e71ec-c0a1-49a8-82d7-bcb317b45860	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS	1
133	16	PALEOCLIMATE INDICATORS	c9a5b3eb-7556-41a8-a2b8-c015db80e5b2	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS	1
134	16	SUN-EARTH INTERACTIONS	3d64c047-c4fb-4981-bc91-d5dbc22337de	EARTH SCIENCE > CLIMATE INDICATORS > SUN-EARTH INTERACTIONS	1
135	16	TERRESTRIAL HYDROSPHERE INDICATORS	9246fc12-17e7-4473-b9c0-c23e4bfc4eda	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS	1
136	17	FROZEN GROUND	376a1d5c-2496-4381-981f-bc047af92044	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND	1
137	17	GLACIERS/ICE SHEETS	8603db51-3484-4439-8b3b-a06f48e8c686	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS	1
138	17	SEA ICE	860e2af9-ce29-4f3f-b027-ae3747eb3e01	EARTH SCIENCE > CRYOSPHERE > SEA ICE	1
139	17	SNOW/ICE	aa35a52f-e3d9-41bd-abd2-ec7e1a8101d1	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE	1
140	18	BOUNDARIES	07a856fd-75e2-46e8-91eb-8a8562d3452f	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES	1
141	18	ECONOMIC RESOURCES	cdbe5ef5-408d-489d-b6ff-4482ce4a99c7	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES	1
142	18	ENVIRONMENTAL GOVERNANCE/MANAGEMENT	d81b77be-0177-4e26-942c-aa911239482d	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT	1
143	18	ENVIRONMENTAL IMPACTS	3f4cfc81-7745-43d9-b313-f68cdf72359b	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS	1
144	18	HABITAT CONVERSION/FRAGMENTATION	f1682ed1-2d9c-41ec-9553-49b9ab55df9b	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION	1
145	18	HUMAN SETTLEMENTS	fee25cad-7ffe-4ee2-a6f2-8116b8a0a707	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS	1
146	18	INFRASTRUCTURE	d4313915-2d24-424c-a171-30ee9a6f4bb5	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE	1
147	18	NATURAL HAZARDS	ec0e2762-f57a-4fdc-b395-c8d7d5590d18	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS	1
148	18	POPULATION	085edf65-1c8c-414a-b8e4-a1a08ff08f22	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION	1
149	18	PUBLIC HEALTH	da2c70fd-d92b-45be-b159-b2c10cb387c6	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH	1
150	18	SOCIAL BEHAVIOR	c8317644-4cb2-4e37-b536-c762f7e670ab	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR	1
151	18	SOCIOECONOMICS	a96e6cd6-0f35-491d-8198-7551d03e1cbc	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIOECONOMICS	1
152	18	SUSTAINABILITY	03d38261-1c90-491b-bc4e-cc4e703e1dff	EARTH SCIENCE > HUMAN DIMENSIONS > SUSTAINABILITY	1
153	19	EROSION/SEDIMENTATION	a246a8cf-e3f9-4045-af9f-dc97f6fe019a	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION	1
154	19	FROZEN GROUND	8073b62d-a2f3-4ad9-b619-de26f28877a7	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND	1
155	19	GEOMORPHIC LANDFORMS/PROCESSES	d35b9ba5-d018-48a5-8f0d-92b9c55b3279	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES	1
156	19	LAND USE/LAND COVER	e5815f58-8232-4c7f-b50d-ea71d73891a9	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER	1
157	19	LANDSCAPE	f36d71c6-f2ad-49c4-809f-09b4f0688412	EARTH SCIENCE > LAND SURFACE > LANDSCAPE	1
158	19	SOILS	3526afb8-0dc9-43c7-8ad4-f34f250a1e91	EARTH SCIENCE > LAND SURFACE > SOILS	1
159	19	SURFACE RADIATIVE PROPERTIES	cb5cc628-a1b5-459e-934f-881153a937b8	EARTH SCIENCE > LAND SURFACE > SURFACE RADIATIVE PROPERTIES	1
160	19	SURFACE THERMAL PROPERTIES	a228b67f-0791-470b-a4ca-71b8da279332	EARTH SCIENCE > LAND SURFACE > SURFACE THERMAL PROPERTIES	1
161	19	TOPOGRAPHY	3e822484-c94a-457b-a32f-376fcbd6fd35	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY	1
162	20	AQUATIC SCIENCES	f27ad52c-3dfd-4788-851a-427e60ae1b8f	EARTH SCIENCE > OCEANS > AQUATIC SCIENCES	1
163	20	BATHYMETRY/SEAFLOOR TOPOGRAPHY	c16bda61-353b-4668-af2f-bbb98785b6fa	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY	1
164	20	COASTAL PROCESSES	b6fd22ab-dca7-4dfa-8812-913453b5695b	EARTH SCIENCE > OCEANS > COASTAL PROCESSES	1
165	20	MARINE ENVIRONMENT MONITORING	ca154e02-a226-4cc7-8e4a-4474e7eb1eeb	EARTH SCIENCE > OCEANS > MARINE ENVIRONMENT MONITORING	1
166	20	MARINE GEOPHYSICS	bb04ee83-bf49-4f96-898d-20bb6e92bc93	EARTH SCIENCE > OCEANS > MARINE GEOPHYSICS	1
167	20	MARINE SEDIMENTS	ce4b2c6e-3d69-4cf1-8416-c36e5f9b1b2c	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS	1
168	20	MARINE VOLCANISM	e3b178eb-2d47-41db-aba1-43a05e9e9256	EARTH SCIENCE > OCEANS > MARINE VOLCANISM	1
169	20	OCEAN ACOUSTICS	0517ae1f-7617-4f3b-80cb-649178032825	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS	1
170	20	OCEAN CHEMISTRY	6eb3919b-85ce-4988-8b78-9d0018fd8089	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY	1
171	20	OCEAN CIRCULATION	a031952d-9f00-4ba5-9966-5f87ab9dfdd4	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION	1
172	20	OCEAN HEAT BUDGET	63bc0693-52eb-4ebd-a39e-e77e96409072	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET	1
175	20	OCEAN TEMPERATURE	251c87cd-03b3-464f-8390-8ede2fec28fc	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE	1
176	20	OCEAN WAVES	a04804d5-1064-48fd-a7a7-8da8e10399e1	EARTH SCIENCE > OCEANS > OCEAN WAVES	1
177	20	OCEAN WINDS	346cade5-801a-4afc-9652-48d02905bc4f	EARTH SCIENCE > OCEANS > OCEAN WINDS	1
178	20	SALINITY/DENSITY	a46016d7-e571-403a-ab37-7223fd74e68e	EARTH SCIENCE > OCEANS > SALINITY/DENSITY	1
179	20	SEA ICE	d73e969a-4b66-4713-8d63-fa3cbb1e25e3	EARTH SCIENCE > OCEANS > SEA ICE	1
180	20	SEA SURFACE TOPOGRAPHY	68f93a0c-1525-4f5a-9545-5d94191a3dbf	EARTH SCIENCE > OCEANS > SEA SURFACE TOPOGRAPHY	1
181	20	TIDES	e3bef663-6116-4f15-995c-38c7cdc9652c	EARTH SCIENCE > OCEANS > TIDES	1
182	20	WATER QUALITY	1ee8a323-f0ba-4a21-b597-50890c527c8e	EARTH SCIENCE > OCEANS > WATER QUALITY	1
183	21	ICE CORE RECORDS	dba19648-3f52-48ba-b00b-8527d44c4d74	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS	1
184	21	LAND RECORDS	486f2c33-2401-4292-9d74-8756ee95211f	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS	1
185	21	OCEAN/LAKE RECORDS	45325a01-2522-48d3-bffa-0edf1a934d48	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS	1
186	21	PALEOCLIMATE RECONSTRUCTIONS	350c9923-fa80-4f83-8724-2886ac559ac0	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS	1
187	22	EARTH GASES/LIQUIDS	e3fa1998-b003-4d55-a92e-16b42ac0fc17	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS	1
188	22	GEOCHEMISTRY	906e647b-2683-4ae7-9986-1aea15582b52	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY	1
189	22	GEODETICS	5498572c-aaed-4c08-8aad-8b297057e9c9	EARTH SCIENCE > SOLID EARTH > GEODETICS	1
190	22	GEOMAGNETISM	910013d7-1e6a-4d1a-9921-be32d792a290	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM	1
191	22	GEOMORPHIC LANDFORMS/PROCESSES	b5cb1fab-7281-478f-bb3b-ff04f900b3fc	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES	1
192	22	GEOTHERMAL DYNAMICS	ec2bf43d-2525-439e-bbbe-0db758e71965	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS	1
193	22	GRAVITY/GRAVITATIONAL FIELD	221386f6-ef9b-4990-82b3-f990b0fe39fa	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD	1
194	22	ROCKS/MINERALS/CRYSTALS	ba8d7f68-ad3a-4874-bc75-312b24b1b1ac	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS	1
195	22	TECTONICS	1e17c8d3-81d0-473c-8f24-d2a4ea52b6b9	EARTH SCIENCE > SOLID EARTH > TECTONICS	1
196	23	GAMMA RAY	0a81d67a-102b-4611-a38c-dbfdd7ba4e7d	EARTH SCIENCE > SPECTRAL/ENGINEERING > GAMMA RAY	1
197	23	INFRARED WAVELENGTHS	7a73c724-b532-45eb-a9a5-c77330b61bab	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS	1
198	23	LIDAR	6182be8b-d006-4327-994d-6f27c7e4d9a9	EARTH SCIENCE > SPECTRAL/ENGINEERING > LIDAR	1
199	23	MICROWAVE	66700628-2b62-4466-999e-faeb15ca4da5	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE	1
200	23	PLATFORM CHARACTERISTICS	cda9b483-8711-42b8-82f9-e7d22ce9c62c	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS	1
201	23	RADAR	d3b7c3c0-e644-4f01-94da-dfebe854c0d1	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR	1
202	23	RADIO WAVE	d7ef7608-01f5-4e95-9fd9-7dc2aa36113d	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADIO WAVE	1
203	23	SENSOR CHARACTERISTICS	8799f524-e313-4d2d-9428-8d672d123513	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS	1
204	23	ULTRAVIOLET WAVELENGTHS	0f36cd66-d755-4809-ad0e-d67b1b9aff6c	EARTH SCIENCE > SPECTRAL/ENGINEERING > ULTRAVIOLET WAVELENGTHS	1
205	23	VISIBLE WAVELENGTHS	c5ff6f39-0c35-488a-96f2-f3498c678e45	EARTH SCIENCE > SPECTRAL/ENGINEERING > VISIBLE WAVELENGTHS	1
206	23	X-RAY	12156f9d-9731-446e-b9de-a781af653b1c	EARTH SCIENCE > SPECTRAL/ENGINEERING > X-RAY	1
207	24	IONOSPHERE/MAGNETOSPHERE DYNAMICS	3a942e8a-d2f2-42bf-9e83-b7b3793b100e	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS	1
208	24	SOLAR ACTIVITY	2e83362e-d8f8-4bca-83fd-bae360ebe94b	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY	1
209	24	SOLAR ENERGETIC PARTICLE FLUX	cad91f82-7e2a-43b7-b272-2dc77e2791f4	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX	1
210	24	SOLAR ENERGETIC PARTICLE PROPERTIES	a82d885e-34cd-496a-b34d-17a23ad04126	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES	1
211	25	GLACIERS/ICE SHEETS	099ab1ae-f4d2-48cc-be2f-86bd58ffc4ca	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS	1
212	25	GROUND WATER	734f8f27-6976-4b67-8794-c7fc79d6161e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER	1
213	25	SNOW/ICE	50b8fe04-9149-4b7f-a8b2-b33b1e3aa192	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE	1
214	25	SURFACE WATER	5debb283-51e4-435e-b2a2-e8e2a977220d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER	1
215	25	WATER QUALITY/WATER CHEMISTRY	8c02f5d1-ce86-4bf5-84d5-b3496cdba6ad	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY	1
4956	26	CALIBRATION	ecf29317-bd5e-447b-b911-f8bfb153c83b	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > CALIBRATION/VALIDATION > CALIBRATION	1
4957	27	DESKTOP GEOGRAPHIC INFORMATION SYSTEMS	565cb301-44de-446c-8fe3-4b5cce428315	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > GEOGRAPHIC INFORMATION SYSTEMS > DESKTOP GEOGRAPHIC INFORMATION SYSTEMS	1
4958	27	MOBILE GEOGRAPHIC INFORMATION SYSTEMS	0dd83b2a-e83f-4a0c-a1ff-2fbdbbcce62d	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > GEOGRAPHIC INFORMATION SYSTEMS > MOBILE GEOGRAPHIC INFORMATION SYSTEMS	1
4959	27	WEB-BASED GEOGRAPHIC INFORMATION SYSTEMS	037f42a2-cdda-4b72-b49c-bdec74d03e0a	EARTH SCIENCE SERVICES > DATA ANALYSIS AND VISUALIZATION > GEOGRAPHIC INFORMATION SYSTEMS > WEB-BASED GEOGRAPHIC INFORMATION SYSTEMS	1
4960	35	DATA REFORMATTING	dad75074-b2f7-4cb7-ae02-02d054f18251	EARTH SCIENCE SERVICES > DATA MANAGEMENT/DATA HANDLING > DATA INTEROPERABILITY > DATA REFORMATTING	1
4961	42	BACKGROUND INFORMATION	1a2f59f6-76f3-4c57-b70b-de350708426f	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > CURRICULUM SUPPORT > BACKGROUND INFORMATION	1
4962	42	CLASSROOM ACTIVITIES	f85293fe-eb9d-491a-bba8-46261a38b9bf	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > CURRICULUM SUPPORT > CLASSROOM ACTIVITIES	1
4963	42	LESSON PLANS	fc889d75-41f3-4f36-b461-1100536c8f50	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > CURRICULUM SUPPORT > LESSON PLANS	1
4964	43	MUSEUM EXHIBITS	24b7bc59-3f10-4a0b-b9c1-92ae10feb007	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > EXHIBIT MATERIALS > MUSEUM EXHIBITS	1
4965	43	SCIENCE CENTER EXHIBITS	fb3b3728-a6ff-465d-8a33-2619a3276cdf	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > EXHIBIT MATERIALS > SCIENCE CENTER EXHIBITS	1
4966	44	STAND-ALONE INTERACTIVE PROGRAMS	bfdcc74d-5e53-44e8-bc0e-5170cfa6152c	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > INTERACTIVE PROGRAMS > STAND-ALONE INTERACTIVE PROGRAMS	1
4967	44	WEB-BASED INTERACTIVE PROGRAMS	cd8bdd2c-a0db-4202-b10d-a1760d834700	EARTH SCIENCE SERVICES > EDUCATION/OUTREACH > INTERACTIVE PROGRAMS > WEB-BASED INTERACTIVE PROGRAMS	1
4968	45	CROP FORECAST	f1c35c74-0b10-46de-9c06-efeda92d383a	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > AGRICULTURAL ADVISORIES > CROP FORECAST	1
4969	45	DROUGHT FORECAST	a394776f-b658-44de-b952-90f4e53d58cc	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > AGRICULTURAL ADVISORIES > DROUGHT FORECAST	1
4970	46	PRESCRIBED BURNS	8de8b909-8fcb-4ed7-9df3-37f9dd54054f	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > FIRE ADVISORIES > PRESCRIBED BURNS	1
4971	46	WILDFIRES	855dc9f5-ccbf-4972-8828-41e11f2aca7a	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > FIRE ADVISORIES > WILDFIRES	1
4972	47	EARTHQUAKES	a779ee72-d21e-4106-9efa-93e970bc287f	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > GEOLOGICAL ADVISORIES > EARTHQUAKES	1
4973	47	GEOMAGNETISM	8f9d66e9-f65d-41c6-9640-90bd3e155bf8	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > GEOLOGICAL ADVISORIES > GEOMAGNETISM	1
4974	47	LANDSLIDES	a8f6e91f-7875-4597-8ab8-64f4b14e8b49	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > GEOLOGICAL ADVISORIES > LANDSLIDES	1
4975	47	VOLCANIC ACTIVITY	f342683b-94ee-4ef6-8915-b18a473fafbd	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > GEOLOGICAL ADVISORIES > VOLCANIC ACTIVITY	1
4976	48	ANIMAL HEALTH ADVISORIES	bcb42cdb-0ad3-42e1-ac72-8af05c68cf48	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HEALTH ADVISORIES > ANIMAL HEALTH ADVISORIES	1
4977	48	DISEASE/EPIDEMIC	8cc052a0-314a-408d-8c2d-c8245bab2465	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HEALTH ADVISORIES > DISEASE/EPIDEMIC	1
4978	48	HUMAN HEALTH ADVISORIES	5e468bd6-a13a-4f49-8cb4-7a0ba69d8ad3	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HEALTH ADVISORIES > HUMAN HEALTH ADVISORIES	1
4979	49	AVALANCHE FORECASTS	b28c7543-e313-43e5-8a27-2d84098d2e11	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HYDROLOGICAL ADVISORIES > AVALANCHE FORECASTS	1
4980	49	DROUGHT	3678d18c-9dca-4743-abc0-1442b4d438d2	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HYDROLOGICAL ADVISORIES > DROUGHT	1
4981	49	FLOODS	e757b032-bfa4-4976-b98a-838f61a86ea8	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HYDROLOGICAL ADVISORIES > FLOODS	1
4982	49	WATER QUALITY	9a583e74-34e9-4eb5-af7a-03418d702af6	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > HYDROLOGICAL ADVISORIES > WATER QUALITY	1
4983	50	MARINE BIOLOGY	3de6fa74-bb80-4bc6-ae60-1e6fe8ae6c67	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > MARINE BIOLOGY	1
4984	50	MARINE WEATHER/FORECAST	c1111b23-9946-497a-8829-b58da3fce720	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > MARINE WEATHER/FORECAST	1
4985	50	OCEAN TEMPERATURE	c5563d03-2f68-4dac-a50b-3b8450725356	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > OCEAN TEMPERATURE	1
4986	50	SEA ICE	a4aea007-d297-4051-8b41-5cdde00b4d1e	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > SEA ICE	1
4987	50	SEA STATE	f04be06d-5976-43d0-94cb-91d5c487d57c	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > SEA STATE	1
4988	50	TIDES	d8aee072-097c-496f-8fe7-b65605fc1103	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > TIDES	1
4989	50	TSUNAMIS	6ee1f87a-dc7a-48f7-9b0f-9c529a5645a5	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > MARINE ADVISORIES > TSUNAMIS	1
4990	51	AURORA FORECASTS	94bafe5f-b97e-49b3-ad62-494865b799f3	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > AURORA FORECASTS	1
4991	51	CORONAL MASS EJECTION	b40d8d03-6286-48cd-818c-20d1680d6453	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > CORONAL MASS EJECTION	1
4992	51	GEOMAGNETIC STORM	ed49aea3-c1ce-4522-985b-1b1b2b2c7790	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > GEOMAGNETIC STORM	1
4993	51	RADIO BLACKOUTS	8cc74c57-9a5e-4f71-a918-73746c150bd3	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > RADIO BLACKOUTS	1
4994	51	SOLAR FLARES	6e039ab2-beed-4b17-9fb2-41965839f5bf	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > SOLAR FLARES	1
4995	51	SOLAR RADIATION STORMS	3b786f1b-aca7-437b-bd86-44f20789da7b	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > SOLAR RADIATION STORMS	1
4996	51	SOLAR WINDS	65475fcc-b696-4b02-a812-f12364046c4c	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > SPACE WEATHER ADVISORIES > SOLAR WINDS	1
4997	52	AIR QUALITY	49c8e881-7100-42cf-9c2e-48f2012e5671	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > AIR QUALITY	1
4998	52	CLIMATE ADVISORIES	392ff7f6-dcf6-4543-930e-3e6e441ad881	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > CLIMATE ADVISORIES	1
4999	52	DUST/ASH ADVISORIES	8f7c2388-24e4-4f90-a833-6dc166693879	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > DUST/ASH ADVISORIES	1
5000	52	FROST/FREEZE WARNING	fb47fa33-8b9b-4655-b448-1acf8a629015	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > FROST/FREEZE WARNING	1
5001	52	HEAT ADVISORY	10144249-d836-4a7d-adc8-177702595c87	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > HEAT ADVISORY	1
5002	52	PRESENT WEATHER	020585ff-91fb-421b-ba24-305d657c2231	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > PRESENT WEATHER	1
5003	52	SEVERE WEATHER	0d67baa7-19c7-440b-b658-1bda9a8e09bf	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > SEVERE WEATHER	1
5004	52	UV RADIATION	e6c260ca-4f1e-4ed9-92d8-b50d1927f88e	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > UV RADIATION	1
5005	52	WEATHER FORECAST	0451cbfb-3c46-4afe-b02d-456beabd89a6	EARTH SCIENCE SERVICES > ENVIRONMENTAL ADVISORIES > WEATHER/CLIMATE ADVISORIES > WEATHER FORECAST	1
5006	55	BIOLOGICAL HAZARDS MAPPING	39a63377-02d8-41a7-814a-41ea7db700c9	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING > BIOLOGICAL HAZARDS MAPPING	1
5091	100	FOOD STORAGE	b3b14df8-5197-4a26-ae61-882fdba706f3	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD STORAGE	1
5007	55	GEOPHYSICAL HAZARDS MAPPING	b32eb466-3fc1-4a03-8011-99002f5591cb	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING > GEOPHYSICAL HAZARDS MAPPING	1
5008	55	HYDROLOGICAL HAZARDS MAPPING	764e3842-9c3c-4d01-a390-fbccfaa81884	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING > HYDROLOGICAL HAZARDS MAPPING	1
5009	55	METEOROLOGICAL HAZARDS MAPPING	9a62a72d-8774-4f52-94e2-f9ad63ce34bd	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING > METEOROLOGICAL HAZARDS MAPPING	1
5010	55	TECHNOLOGICAL HAZARDS MAPPING	d454b0f7-d811-46b4-9778-45bb60d7c914	EARTH SCIENCE SERVICES > HAZARDS MANAGEMENT > HAZARDS MAPPING > TECHNOLOGICAL HAZARDS MAPPING	1
5011	62	MODEL LOGS	108318e6-89c0-4e0d-bcad-7bfdb0df49f5	EARTH SCIENCE SERVICES > MODELS > ANCILLARY MODELS > MODEL LOGS	1
5012	83	BIBLIOGRAPHIC DATABASES	6ee8d84e-c829-44e2-8768-3e5342b79707	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > BIBLIOGRAPHIC > BIBLIOGRAPHIC DATABASES	1
5013	83	PERSONNEL DIRECTORIES	17d6617a-10ff-45b6-ac16-a7ab8f6aa1eb	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > BIBLIOGRAPHIC > PERSONNEL DIRECTORIES	1
5014	83	PROFESSIONAL SCIENTIFIC ORGANIZATIONS	2a00621f-4e28-4d16-a183-0658e95d473a	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > BIBLIOGRAPHIC > PROFESSIONAL SCIENTIFIC ORGANIZATIONS	1
5015	84	ASK-A BIOLOGIST	e12352e3-0312-4c12-b62b-25e147193b78	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A BIOLOGIST	1
5016	84	ASK-A ECOLOGIST	185f7a64-7c35-4e83-b0f0-7f2012e66c5d	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A ECOLOGIST	1
5017	84	ASK-A GEOLOGIST	c62eddd4-a320-4f5d-8f9c-5f333be0b7c3	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A GEOLOGIST	1
5018	84	ASK-A MARINE BIOLOGIST	1ee9dd80-6ca8-49a9-a7be-bd965595e1a3	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A MARINE BIOLOGIST	1
5019	84	ASK-A METEOROLOGIST	a9586b25-36da-4e7d-ac2a-b1b24e2f44bd	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A METEOROLOGIST	1
5020	84	ASK-A OCEANOGRAPHER	6621ba11-af39-4634-b07c-811585e91a77	EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A OCEANOGRAPHER	1
5021	90	CHAIN DEFINITION SERVICES	83cfde01-9ed0-44df-a606-4bcd7350706c	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > CHAIN DEFINITION SERVICES	1
5022	90	COVERAGE GENERALIZATION SERVICES	62d7c667-997a-4a9d-abe1-4cca4519673e	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > COVERAGE GENERALIZATION SERVICES	1
5023	90	FEATURE GENERALIZATION APPLICATION SERVICES	e8087aa7-142f-44d3-ad6e-0a75f17b091e	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > FEATURE GENERALIZATION APPLICATION SERVICES	1
5024	90	GAZETTEER APPLICATION SERVICES	1ef01bb2-eba5-41ee-b385-8c36e477d286	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > GAZETTEER APPLICATION SERVICES	1
5025	90	GEOGRAPHIC DATA DISCOVERY SERVICES	9047c8f5-3e5a-4073-8cf5-7f4d5ef783d1	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > GEOGRAPHIC DATA DISCOVERY SERVICES	1
5026	90	GEOGRAPHIC DATA EXTRACTION SERVICES	617a50aa-5762-4ff3-aa03-c94b5cc65209	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > GEOGRAPHIC DATA EXTRACTION SERVICES	1
5027	90	GEOGRAPHIC DATA MANAGEMENT SERVICES	75fbafb0-1f0e-47b3-a9c7-e56dea4b0e91	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > GEOGRAPHIC DATA MANAGEMENT SERVICES	1
5028	90	WEB PORTAL SERVICES	6d77e9d1-d2d1-4b57-a313-0e01e22f799d	EARTH SCIENCE SERVICES > WEB SERVICES > DATA APPLICATION SERVICES > WEB PORTAL SERVICES	1
5029	91	CHANGE DETECTION SERVICES	4b5c0805-13ec-4d32-81ae-430265d15f49	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > CHANGE DETECTION SERVICES	1
5030	91	COVERAGE GENERALIZATION SERVICES	91e02d43-bf56-480f-89c9-ddfca7fc7239	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > COVERAGE GENERALIZATION SERVICES	1
5031	91	COVERAGE PORTRAYAL SERVICE	72b3df24-a061-4624-ad62-f3794798136c	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > COVERAGE PORTRAYAL SERVICE	1
5032	91	DATA ALIGNMENT SERVICES	c8390ac2-4124-43e7-a83e-87cf5eb40f0e	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > DATA ALIGNMENT SERVICES	1
5033	91	DIMENSION MEASUREMENT SERVICES	c53868ba-608c-495c-a65d-038f53f7267f	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > DIMENSION MEASUREMENT SERVICES	1
5034	91	FEATURE GENERALIZATION SERVICES	df6cc99d-6254-4759-91bd-3233b6419b4c	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > FEATURE GENERALIZATION SERVICES	1
5035	91	FEATURE PORTRAYAL SERVICE	af95fcef-dbe1-4dbf-9969-1e6ca75e7f5c	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > FEATURE PORTRAYAL SERVICE	1
5036	91	FORMAT CONVERSION SERVICES	85b1ed02-700a-4591-b2f7-c997a676332c	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > FORMAT CONVERSION SERVICES	1
5384	126	POLLEN	b0ad34ee-4b38-4a8d-a483-b3bfea66fa82	EARTH SCIENCE > BIOSPHERE > VEGETATION > POLLEN	1
5037	91	GEOCODER SERVICE	d55c5f36-4965-441f-8141-9a3faa17297b	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > GEOCODER SERVICE	1
5038	91	GEOGRAPHIC DATA EXTRACTION SERVICES	dccb7a1b-91d6-43d8-bb9d-ffb5778a17a3	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > GEOGRAPHIC DATA EXTRACTION SERVICES	1
5039	91	GEOLINKED DATA ACCESS SERVICE	8ca62ed6-d6e9-4ab0-97ef-138b0f83f597	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > GEOLINKED DATA ACCESS SERVICE	1
5040	91	GEOLINKING SERVICE	2a2db13c-c86d-40ea-9fa8-6d2d5bdac08e	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > GEOLINKING SERVICE	1
5041	91	GEOPARSER SERVICE	250cc56c-2edf-4774-8970-d69a17f15e97	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > GEOPARSER SERVICE	1
5042	91	PROXIMITY ANALYSIS SERVICES	ceeb019c-84d0-4353-b311-04b5a7e305a7	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > PROXIMITY ANALYSIS SERVICES	1
5043	91	SEMANTIC TRANSLATION SERVICES	a2476ff7-0d19-4db9-9834-956351cb0f3e	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > SEMANTIC TRANSLATION SERVICES	1
5044	91	WEB 3D SERVICE	4a07f23e-e3f7-4cda-880f-c8cdc6b33e37	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > WEB 3D SERVICE	1
5045	91	WEB COORDINATE TRANSFORMATION SERVICE	ff889b84-e12f-40ab-815b-61d5aecf2b63	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > WEB COORDINATE TRANSFORMATION SERVICE	1
5046	91	WEB IMAGE CLASSIFICATION SERVICE	0cf44d92-1959-41af-9890-b916008efbae	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > WEB IMAGE CLASSIFICATION SERVICE	1
5047	91	WEB TERRAIN SERVICE	bb0e3a35-d81e-4741-9c0e-3b77bc409cf8	EARTH SCIENCE SERVICES > WEB SERVICES > DATA PROCESSING SERVICES > WEB TERRAIN SERVICE	1
5048	92	CATALOG SERVICE FOR THE WEB	cabd97d6-aa6c-48b8-963b-79248634ce5d	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > CATALOG SERVICE FOR THE WEB	1
5049	92	GAZETTEER SERVICE	73098e85-81ed-4556-93ca-ac1e4f4884ab	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > GAZETTEER SERVICE	1
5050	92	UNIVERSAL DESCRIPTION, DISCOVERY AND INTEGRATION (UDDI) SERVICE	f2115645-e006-414a-bfb6-083d4874a665	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > UNIVERSAL DESCRIPTION, DISCOVERY AND INTEGRATION (UDDI) SERVICE	1
5051	92	WEB COVERAGE SERVICE	d6379bf5-88dd-4ec0-9b15-441db5b10b59	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > WEB COVERAGE SERVICE	1
5052	92	WEB FEATURE SERVICE	d2e9b10f-3b62-42fb-b906-7b4779170a4a	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > WEB FEATURE SERVICE	1
5053	92	WEB MAP SERVICE	cdb4a032-bb7d-455d-b3dc-e88fa465b7c7	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > WEB MAP SERVICE	1
5054	92	WEB PROCESSING SERVICES	933bf0ab-11af-40df-a9d9-1b4a809edd87	EARTH SCIENCE SERVICES > WEB SERVICES > INFORMATION MANAGEMENT SERVICES > WEB PROCESSING SERVICES	1
5055	93	AQUACULTURE	8916dafb-5ad5-45c6-ab64-3500ea1e9577	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL AQUATIC SCIENCES > AQUACULTURE	1
5056	93	FISHERIES	c7112a64-be39-414a-9125-f63ab44ecb5b	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL AQUATIC SCIENCES > FISHERIES	1
5057	93	TEST	0916afef-a0b7-4ecd-85ba-cc24070470a7	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL AQUATIC SCIENCES > TEST	1
5058	94	FERTILIZERS	18a8197e-3a3f-408c-9c51-e9fe89dd6b45	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL CHEMICALS > FERTILIZERS	1
5059	94	PESTICIDES	59a203f9-f818-42a6-8d00-4301385cafc3	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL CHEMICALS > PESTICIDES	1
5060	95	AGRICULTURAL EQUIPMENT	f2f37978-d942-43d2-9c51-79e9f5bdfe24	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL ENGINEERING > AGRICULTURAL EQUIPMENT	1
5061	95	FARM STRUCTURES	d53e1951-fb68-4ad8-8725-d19c10751da5	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL ENGINEERING > FARM STRUCTURES	1
5062	96	CROP/PLANT YIELDS	f12d8026-f24a-4413-91d0-4704c243c9e7	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > CROP/PLANT YIELDS	1
5063	96	CROPPING SYSTEMS	2dda92a8-6c26-4506-9881-43b6d9a83b18	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > CROPPING SYSTEMS	1
5064	96	IRRIGATION	a756fd6b-6208-4af0-ac56-6ee914fc4597	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > IRRIGATION	1
5065	96	PLANT BREEDING AND GENETICS	dcd7a439-6021-4fc3-b3d8-a8936ef171f6	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > PLANT BREEDING AND GENETICS	1
5066	96	PLANT DISEASES/DISORDERS/PESTS	213cefd8-806f-40f5-b3ca-05022cde9498	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > PLANT DISEASES/DISORDERS/PESTS	1
5067	96	RECLAMATION/REVEGETATION/RESTORATION	c7570528-f2d5-42b0-b8e9-d12a2432e87e	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > RECLAMATION/REVEGETATION/RESTORATION	1
5068	96	WEEDS, NOXIOUS PLANTS OR INVASIVE PLANTS	b376a9f9-585e-4567-ba1f-55ef45cfa8df	EARTH SCIENCE > AGRICULTURE > AGRICULTURAL PLANT SCIENCE > WEEDS, NOXIOUS PLANTS OR INVASIVE PLANTS	1
5069	97	DAIRY PRODUCTS	a368da76-b191-4859-bd55-8643f4fab812	EARTH SCIENCE > AGRICULTURE > ANIMAL COMMODITIES > DAIRY PRODUCTS	1
5070	97	LIVESTOCK PRODUCTS	1e2557c5-d232-48e4-8276-369a22ae6aae	EARTH SCIENCE > AGRICULTURE > ANIMAL COMMODITIES > LIVESTOCK PRODUCTS	1
5071	97	POULTRY PRODUCTS	d3ce1677-f3a8-452e-91c8-0ff80e6a3f09	EARTH SCIENCE > AGRICULTURE > ANIMAL COMMODITIES > POULTRY PRODUCTS	1
5072	98	ANIMAL BREEDING AND GENETICS	26089a3e-469d-44b3-a9aa-231d0a072ef9	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL BREEDING AND GENETICS	1
5073	98	ANIMAL DISEASES/DISORDERS/PESTS	e749bafe-9a0a-42cc-bed8-9b42e3e088c8	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL DISEASES/DISORDERS/PESTS	1
5074	98	ANIMAL ECOLOGY AND BEHAVIOR	5d1b53b2-7d69-4b7c-903f-d8cf29430f93	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL ECOLOGY AND BEHAVIOR	1
5075	98	ANIMAL MANAGEMENT SYSTEMS	e5b724af-b661-406a-ae1f-7cd2730c0576	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL MANAGEMENT SYSTEMS	1
5076	98	ANIMAL MANURE AND WASTE	3c1c65c3-e1ef-4163-9695-c39ff7fb48da	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL MANURE AND WASTE	1
5077	98	ANIMAL NUTRITION	ca551e61-4b8c-46d5-8590-80cada40ebbd	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL NUTRITION	1
5078	98	ANIMAL PHYSIOLOGY AND BIOCHEMISTRY	f9cdf3ae-fe8b-4a19-a946-a8c8780d7894	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL PHYSIOLOGY AND BIOCHEMISTRY	1
5079	98	ANIMAL YIELDS	3c0bbd0f-6d4d-4036-afa9-03f9b4f8fba0	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > ANIMAL YIELDS	1
5080	98	APICULTURE	2c31fc22-747a-476f-b76d-fec61220b5b1	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > APICULTURE	1
5081	98	SERICULTURE	06053150-d796-477b-b305-292442d658ed	EARTH SCIENCE > AGRICULTURE > ANIMAL SCIENCE > SERICULTURE	1
5082	99	FEED COMPOSITION	cf9ef34d-ed39-4c8d-bf00-ca1b0bb11363	EARTH SCIENCE > AGRICULTURE > FEED PRODUCTS > FEED COMPOSITION	1
5083	99	FEED CONTAMINATION AND TOXICOLOGY	b9957bbc-3c12-481d-86a0-0f6cf2bb8219	EARTH SCIENCE > AGRICULTURE > FEED PRODUCTS > FEED CONTAMINATION AND TOXICOLOGY	1
5084	99	FEED PROCESSING	fec2eb53-bc69-4d35-849c-c2bedf5dc6cf	EARTH SCIENCE > AGRICULTURE > FEED PRODUCTS > FEED PROCESSING	1
5085	99	FEED STORAGE	9244fe19-b86f-4a8d-82bf-c52f804a77e3	EARTH SCIENCE > AGRICULTURE > FEED PRODUCTS > FEED STORAGE	1
5086	100	FOOD ADDITIVES	eb9b8c19-3b39-4865-bcfc-d2a12689094a	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD ADDITIVES	1
5087	100	FOOD CONTAMINATION AND TOXICOLOGY	e86ea427-f735-4998-af16-9bd619df4974	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD CONTAMINATION AND TOXICOLOGY	1
5088	100	FOOD PACKAGING	85d7c19a-6d05-446f-a490-382e7c199e09	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD PACKAGING	1
5089	100	FOOD PROCESSING	b153bcea-3114-4809-8e6f-f22cf9a3be87	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD PROCESSING	1
5090	100	FOOD QUALITY	3ec3b00e-52e1-4df9-99cd-c93120d97645	EARTH SCIENCE > AGRICULTURE > FOOD SCIENCE > FOOD QUALITY	1
5092	101	AFFORESTATION/REFORESTATION	b3a1e091-0bc2-4c9b-a89c-bd003fdd5889	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > AFFORESTATION/REFORESTATION	1
5093	101	DEFOLIANTS	b3fcccdd-745f-4299-94b3-e72e37f551be	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > DEFOLIANTS	1
5094	101	FOREST CONSERVATION	7ee9d286-0742-4844-b7eb-b7550d3f782b	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST CONSERVATION	1
5095	101	FOREST FIRE SCIENCE	e5a8c6ed-5b59-40fe-a83b-18b39fb7c31b	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST FIRE SCIENCE	1
5096	101	FOREST HARVESTING AND ENGINEERING	23336b57-1ba3-42a6-9ec7-152285c55689	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST HARVESTING AND ENGINEERING	1
5097	101	FOREST MANAGEMENT	d2056285-8249-4c11-810b-783600030525	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST MANAGEMENT	1
5098	101	FOREST MENSURATION	31d01087-d5b8-4474-820c-d84d523dfb39	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST MENSURATION	1
5099	101	FOREST PRODUCTS/COMMODITIES	3676ebab-9aa0-43c2-94e5-5d59a34317d2	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST PRODUCTS/COMMODITIES	1
5100	101	FOREST PROTECTION	adeb4c27-a115-4ced-9827-5f022883f606	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST PROTECTION	1
5101	101	FOREST YIELDS	49804617-d59b-4e97-8030-2c4ab79a3057	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > FOREST YIELDS	1
5102	101	REFORESTATION	be7f6de0-f51e-42bc-9a66-fff30d809a67	EARTH SCIENCE > AGRICULTURE > FOREST SCIENCE > REFORESTATION	1
5103	102	FIELD CROP PRODUCTS	63317fb1-01d9-4658-93e8-9800c5359454	EARTH SCIENCE > AGRICULTURE > PLANT COMMODITIES > FIELD CROP PRODUCTS	1
5104	102	FRUIT PRODUCTS	41b30b1b-5dbb-4ef8-849c-e1949ad04227	EARTH SCIENCE > AGRICULTURE > PLANT COMMODITIES > FRUIT PRODUCTS	1
5105	102	HORTICULTURAL PRODUCTS	d23b37cd-5e05-4356-b8b4-df6d7af236d6	EARTH SCIENCE > AGRICULTURE > PLANT COMMODITIES > HORTICULTURAL PRODUCTS	1
5106	102	VEGETABLE PRODUCTS	eb1627c2-0061-466c-9935-399e53a06024	EARTH SCIENCE > AGRICULTURE > PLANT COMMODITIES > VEGETABLE PRODUCTS	1
5107	103	CALCIUM	7367c08c-304f-4ce7-b716-975f835ba711	EARTH SCIENCE > AGRICULTURE > SOILS > CALCIUM	1
5108	103	CARBON	9315c474-b65f-400d-beba-611c9a6a62cb	EARTH SCIENCE > AGRICULTURE > SOILS > CARBON	1
5109	103	CATION EXCHANGE CAPACITY	5c05e69f-f6db-4296-abd3-3b07e6093579	EARTH SCIENCE > AGRICULTURE > SOILS > CATION EXCHANGE CAPACITY	1
5110	103	DENITRIFICATION RATE	cac79930-334e-49c5-836b-4f2ee8e0b098	EARTH SCIENCE > AGRICULTURE > SOILS > DENITRIFICATION RATE	1
5111	103	ELECTRICAL CONDUCTIVITY	7241d799-4f5c-4ae3-a4ec-2e9cdbf656aa	EARTH SCIENCE > AGRICULTURE > SOILS > ELECTRICAL CONDUCTIVITY	1
5112	103	HEAVY METALS	8b3939b6-1c11-4a79-878e-0be1b231c528	EARTH SCIENCE > AGRICULTURE > SOILS > HEAVY METALS	1
5113	103	HYDRAULIC CONDUCTIVITY	7112e739-cb5d-427e-95bd-5419360e91d8	EARTH SCIENCE > AGRICULTURE > SOILS > HYDRAULIC CONDUCTIVITY	1
5114	103	MACROFAUNA	83da5ac6-5981-4929-9e19-f46522c1babe	EARTH SCIENCE > AGRICULTURE > SOILS > MACROFAUNA	1
5115	103	MAGNESIUM	79f18259-bd76-4c7b-bd18-cbd2edafd24f	EARTH SCIENCE > AGRICULTURE > SOILS > MAGNESIUM	1
5116	103	MICROFAUNA	53231d78-471d-4afe-a435-b577b7d53b17	EARTH SCIENCE > AGRICULTURE > SOILS > MICROFAUNA	1
5117	103	MICROFLORA	b3063d3a-af53-44f9-a532-4cea2880c198	EARTH SCIENCE > AGRICULTURE > SOILS > MICROFLORA	1
5118	103	MICRONUTRIENTS/TRACE ELEMENTS	2473e776-4449-4351-9835-1507532ae60e	EARTH SCIENCE > AGRICULTURE > SOILS > MICRONUTRIENTS/TRACE ELEMENTS	1
5119	103	NITROGEN	5ed7811a-2ba1-4985-9f1c-a78c802fa27f	EARTH SCIENCE > AGRICULTURE > SOILS > NITROGEN	1
5120	103	ORGANIC MATTER	83cf51f6-8c03-4f6d-b605-fde9818c7805	EARTH SCIENCE > AGRICULTURE > SOILS > ORGANIC MATTER	1
5121	103	PERMAFROST	fb3ce3be-d830-407f-bd7c-58d66c24b6be	EARTH SCIENCE > AGRICULTURE > SOILS > PERMAFROST	1
5122	103	PHOSPHORUS	4962dabc-b426-4c84-8147-12e15645baff	EARTH SCIENCE > AGRICULTURE > SOILS > PHOSPHORUS	1
5123	103	POTASSIUM	c07fe67b-234e-4293-9f09-abaf9612c0e9	EARTH SCIENCE > AGRICULTURE > SOILS > POTASSIUM	1
5124	103	RECLAMATION/REVEGETATION/RESTORATION	356a10e1-c81d-44c7-9706-31f7f2642586	EARTH SCIENCE > AGRICULTURE > SOILS > RECLAMATION/REVEGETATION/RESTORATION	1
5125	103	SOIL ABSORPTION	d0da93ff-af45-4e26-8b94-8b90d0e06438	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL ABSORPTION	1
5126	103	SOIL BULK DENSITY	62d5fb39-e9ee-47db-a426-1991537f8a4d	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL BULK DENSITY	1
5127	103	SOIL CHEMISTRY	652349bd-f6f9-4c8d-8573-d71e05ad1208	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL CHEMISTRY	1
5128	103	SOIL CLASSIFICATION	2f57fd58-d8e4-4e6d-b8c3-2a9ef7e64f54	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL CLASSIFICATION	1
5129	103	SOIL COLOR	3985ce6b-e0c3-42a8-b40f-9dd948350c6e	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL COLOR	1
5130	103	SOIL COMPACTION	e0c0af2a-1429-4248-8d5b-ccae510da0c9	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL COMPACTION	1
5131	103	SOIL CONSISTENCE	25c5c222-c053-4081-ac0f-52e6c774198c	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL CONSISTENCE	1
5132	103	SOIL DEPTH	b09b4731-f357-4838-829b-f38c0f5075aa	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL DEPTH	1
5133	103	SOIL EROSION	36c862a7-7117-4fd2-8e33-0dda03097178	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL EROSION	1
5134	103	SOIL FERTILITY	e4781de7-a4a4-4157-a549-4ac238d36512	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL FERTILITY	1
5135	103	SOIL GAS/AIR	d302aeaa-3a86-4ddf-9755-60b7bb4404a5	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL GAS/AIR	1
5136	103	SOIL HEAT BUDGET	68033b72-7f8d-48a4-8f63-638e4e96fd23	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL HEAT BUDGET	1
5137	103	SOIL HORIZONS/PROFILE	1fc22c9d-cf29-4bd7-90b1-b0f6f139fd92	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL HORIZONS/PROFILE	1
5138	103	SOIL IMPEDANCE	6edf1b99-fe00-493e-b0d1-ad6b36b8da75	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL IMPEDANCE	1
5139	103	SOIL INFILTRATION	0ab5ead8-6037-42b3-b3c0-0746f3645af6	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL INFILTRATION	1
5140	103	SOIL MECHANICS	3b1d75b6-7559-4921-8edb-63f4dff370cf	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL MECHANICS	1
5141	103	SOIL MOISTURE/WATER CONTENT	88e1a654-5cfd-423f-9350-0ef48d85e085	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL MOISTURE/WATER CONTENT	1
5142	103	SOIL PH	2a9bce94-c391-4834-96bb-a9685d3590b1	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL PH	1
5143	103	SOIL PLASTICITY	934bfe13-908b-40d9-b346-a347a8a6855e	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL PLASTICITY	1
5144	103	SOIL POROSITY	c26693ea-ca5a-44e8-9e8e-32427bc62aa0	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL POROSITY	1
5145	103	SOIL PRODUCTIVITY	5c6df811-bebf-4dae-a70f-f49fece3fa1e	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL PRODUCTIVITY	1
5146	103	SOIL RESPIRATION	db9b56da-e05f-4d58-b9d5-34edc83ca650	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL RESPIRATION	1
5147	103	SOIL ROOTING DEPTH	2b91245e-a779-42fa-89c2-303217463b95	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL ROOTING DEPTH	1
5148	103	SOIL SALINITY/SOIL SODICITY	3b54403e-25a1-43cc-97ac-7c14e73bda96	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL SALINITY/SOIL SODICITY	1
5149	103	SOIL STRUCTURE	e4daef1d-e672-41d0-bc6d-80c6b5c0799b	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL STRUCTURE	1
5150	103	SOIL TEMPERATURE	26f5bb2a-b872-41e8-922f-3a9a0e9f9bcd	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL TEMPERATURE	1
5151	103	SOIL TEXTURE	afd1d3cb-d31d-4069-8cff-b592887aa18c	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL TEXTURE	1
5152	103	SOIL WATER HOLDING CAPACITY	223ce1f2-e2f1-4612-8fce-b96b7d34710f	EARTH SCIENCE > AGRICULTURE > SOILS > SOIL WATER HOLDING CAPACITY	1
5153	103	SULFUR	e3d3f76d-0ffe-4616-9988-0520e78cf842	EARTH SCIENCE > AGRICULTURE > SOILS > SULFUR	1
5154	103	THERMAL CONDUCTIVITY	5c349776-dd95-483e-a5da-e8d1b1434985	EARTH SCIENCE > AGRICULTURE > SOILS > THERMAL CONDUCTIVITY	1
5155	104	AEROSOL BACKSCATTER	f795b88f-1aba-4548-97f6-7b587e8ba451	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL BACKSCATTER	1
5156	104	AEROSOL EXTINCTION	40633fe2-5b32-4bdc-a17b-b1cfebc01ae7	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL EXTINCTION	1
5157	104	AEROSOL FORWARD SCATTER	449e2e03-8efd-42b6-8152-3602e4bab21d	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL FORWARD SCATTER	1
5158	104	AEROSOL OPTICAL DEPTH/THICKNESS	61c3b720-abc8-4430-866c-f1da35d2cd0b	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL OPTICAL DEPTH/THICKNESS	1
5159	104	AEROSOL PARTICLE PROPERTIES	02ea239e-4bca-4fda-ab87-be12c723c30a	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL PARTICLE PROPERTIES	1
5160	104	AEROSOL RADIANCE	7db9eab3-4c7a-4471-a826-a306f178ad3e	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL RADIANCE	1
5161	104	CARBONACEOUS AEROSOLS	527f637c-aea5-4519-9293-d57e10a76bff	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > CARBONACEOUS AEROSOLS	1
5162	104	CHEMICAL COMPOSITION	0611b9fd-fd92-4c4d-87bb-bc2f22c548bc	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > CHEMICAL COMPOSITION	1
5163	104	CLOUD CONDENSATION NUCLEI	27478148-b4b6-4c89-8829-08d2ee7bfe10	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > CLOUD CONDENSATION NUCLEI	1
5164	104	DUST/ASH/SMOKE	1b6342c6-315b-4f4f-b4e3-d6902aaa3e85	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > DUST/ASH/SMOKE	1
5165	104	NITRATE PARTICLES	768cfa32-003d-47bd-ab3a-3e27e4ec2699	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > NITRATE PARTICLES	1
5166	104	ORGANIC PARTICLES	8929113a-ded5-4c39-b20f-7968ed114317	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > ORGANIC PARTICLES	1
5167	104	PARTICULATE MATTER	548a3f85-bf22-473b-b641-45c32d9c6a0c	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > PARTICULATE MATTER	1
5168	104	SULFATE PARTICLES	ca71b02b-4446-414c-8697-0950d7382cc4	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > SULFATE PARTICLES	1
5169	105	CARBON MONOXIDE	080389c4-68d4-41ee-ab89-070794038c8e	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > CARBON MONOXIDE	1
5170	105	EMISSIONS	2a60df4a-a0d7-4e4b-b02a-372a083f0170	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > EMISSIONS	1
5171	105	LEAD	c79453a3-ed2f-4ec4-9298-bf9fd11d08eb	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > LEAD	1
5172	105	NITROGEN OXIDES	e5563c99-0fb6-43a9-8e20-6b47b1144394	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > NITROGEN OXIDES	1
5173	105	PARTICULATES	f9fe1bc0-88c5-4c26-9b4c-a9867d027685	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > PARTICULATES	1
5174	105	SMOG	bad08657-da2b-4e2b-9804-25c5732bc795	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > SMOG	1
5175	105	SULFUR OXIDES	c3090318-c845-4242-bf2f-ff1631b88831	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > SULFUR OXIDES	1
5176	105	TROPOSPHERIC OZONE	426aee98-764c-4c21-ab65-1e9d4bd6b0d0	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > TROPOSPHERIC OZONE	1
5177	105	TURBIDITY	227cf2d4-968a-4312-89e6-8c6bcf616e5d	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > TURBIDITY	1
5178	105	VISIBILITY	9337898d-68dc-43d7-93a9-6afdb4ab1784	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > VISIBILITY	1
5179	105	VOLATILE ORGANIC COMPOUNDS	1f3c543d-9ca9-4db4-b4a5-d3e2fd71e4a4	EARTH SCIENCE > ATMOSPHERE > AIR QUALITY > VOLATILE ORGANIC COMPOUNDS	1
5180	106	BAROMETRIC ALTITUDE	5d703cfe-2f7c-4736-acbc-ec4e4f4f8eef	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > BAROMETRIC ALTITUDE	1
5181	106	GEOPOTENTIAL HEIGHT	d6aec072-daf9-4f96-b667-6c7831cf6bdd	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > GEOPOTENTIAL HEIGHT	1
5182	106	MESOPAUSE	dacbf270-1734-4503-bab8-a32cdaff3012	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > MESOPAUSE	1
5183	106	PLANETARY BOUNDARY LAYER HEIGHT	765e92a7-8c14-47dc-bdd8-d85d132a11ee	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > PLANETARY BOUNDARY LAYER HEIGHT	1
5184	106	STATION HEIGHT	2343baae-1c4a-4096-8cac-fea8ed7a984f	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > STATION HEIGHT	1
5185	106	STRATOPAUSE	82191e97-53ba-413d-9a08-acd8b848e0b0	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > STRATOPAUSE	1
5186	106	TROPOPAUSE	c3447c90-7490-4f04-89c1-c5274ba8f8f6	EARTH SCIENCE > ATMOSPHERE > ALTITUDE > TROPOPAUSE	1
5187	107	CARBON AND HYDROCARBON COMPOUNDS	19ab681c-bdd7-4793-bbdb-1ec498575314	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS	1
5188	126	CHLOROPHYLL	5e3999ec-d864-43fd-8d84-bd23630c405f	EARTH SCIENCE > BIOSPHERE > VEGETATION > CHLOROPHYLL	1
5189	107	HALOCARBONS AND HALOGENS	d46a5046-e1c6-4a09-a2f1-db6a21eda611	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS	1
5190	107	HYDROGEN COMPOUNDS	d8dcfd36-f71c-499f-84f5-43da9fee26c5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HYDROGEN COMPOUNDS	1
5191	107	NITROGEN COMPOUNDS	9e5ec924-2fd3-4cbb-a7eb-ffde114d0cb9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS	1
5192	107	OXYGEN COMPOUNDS	4cc9b4fa-5097-447f-914c-eb90820938c6	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > OXYGEN COMPOUNDS	1
5193	107	PHOTOCHEMISTRY	6433e330-3797-4cf9-a8ba-d26d39624459	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > PHOTOCHEMISTRY	1
5194	107	SULFUR COMPOUNDS	b80a242d-d5f5-4a5f-976c-6f6fe2ab6b2c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS	1
5195	107	TRACE ELEMENTS/TRACE METALS	2d36c283-2fe3-4a08-aeb3-6a8146e79bb3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > TRACE ELEMENTS/TRACE METALS	1
5196	107	TRACE GASES/TRACE SPECIES	4dd22dc9-1db4-4187-a2b7-f5b76d666055	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > TRACE GASES/TRACE SPECIES	1
5197	108	ATMOSPHERIC CONDUCTIVITY	12b1cc7c-cb81-4851-9163-19c04a8ffd1c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC ELECTRICITY > ATMOSPHERIC CONDUCTIVITY	1
5198	108	ELECTRIC FIELD	41f27172-14f6-4940-9b7b-f3d4db69e0c6	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC ELECTRICITY > ELECTRIC FIELD	1
5199	108	LIGHTNING	637ac172-e624-4ae0-aac4-0d1adcc889a2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC ELECTRICITY > LIGHTNING	1
5200	108	TOTAL ELECTRON CONTENT	cac28264-0788-49a9-bb6a-c2251b0b325c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC ELECTRICITY > TOTAL ELECTRON CONTENT	1
5201	109	ANTICYCLONES/CYCLONES	178694aa-5f0a-4de5-a193-74e323dc6aa9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > ANTICYCLONES/CYCLONES	1
5202	109	ATMOSPHERIC PRESSURE MEASUREMENTS	9efbc088-ba8c-4c9c-a458-ad6ad63f4188	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > ATMOSPHERIC PRESSURE MEASUREMENTS	1
5203	109	DIFFERENTIAL PRESSURE	5d7e487d-0ec4-40ef-9811-401779c31794	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > DIFFERENTIAL PRESSURE	1
5204	109	GRAVITY WAVE	7e6f7c15-32e7-4b6e-bd35-7bff4bc03caf	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > GRAVITY WAVE	1
5205	109	HYDROSTATIC PRESSURE	a5aa7055-642d-4442-9b4b-76a759e15257	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > HYDROSTATIC PRESSURE	1
5206	109	OSCILLATIONS	c0656cbc-5d94-4945-bbfd-1c8eabb059b2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > OSCILLATIONS	1
5207	109	PLANETARY BOUNDARY LAYER HEIGHT	f51a3caf-c5ec-496a-8dd3-854d9bb994e7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PLANETARY BOUNDARY LAYER HEIGHT	1
5208	109	PLANETARY/ROSSBY WAVES	6f262b9b-2cb8-4745-ae41-5fff23c72a1e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PLANETARY/ROSSBY WAVES	1
5209	109	PRESSURE ANOMALIES	011bed30-f5b6-4b46-a7ce-797851f24f24	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE ANOMALIES	1
5210	109	PRESSURE TENDENCY	fa98caa0-54dc-465e-9bde-cdf4da905994	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE TENDENCY	1
5211	109	PRESSURE THICKNESS	be027470-35ab-4ebb-a213-5f557cca71c8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > PRESSURE THICKNESS	1
5212	109	SEA LEVEL PRESSURE	07ce145c-9936-4675-b4a7-8710e39aa391	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SEA LEVEL PRESSURE	1
5213	109	STATIC PRESSURE	622c44b4-e307-4c11-af4d-8104de7086e5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > STATIC PRESSURE	1
5214	109	SURFACE PRESSURE	b54de5cd-4475-4c7b-acbc-4eb529b9396e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > SURFACE PRESSURE	1
5215	109	TOPOGRAPHIC WAVES	b13a29a1-47a0-4d8b-a017-398b364dc202	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC PRESSURE > TOPOGRAPHIC WAVES	1
5216	110	ABSORPTION	061f7fd0-67af-42bf-bc9f-5a007c146f65	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ABSORPTION	1
5217	110	ACTINIC FLUX	ec839718-ba64-4bc5-8458-fae7390e11c4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ACTINIC FLUX	1
5218	110	AIRGLOW	bf22e55d-fbff-4eaf-8592-68be24e2bc32	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > AIRGLOW	1
5219	110	ALBEDO	48c16952-b6e0-40cd-b6dd-7cdbf5a443a1	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ALBEDO	1
5220	110	ANISOTROPY	31a14270-6275-4155-961f-b78b60ee05f7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ANISOTROPY	1
5221	110	ATMOSPHERIC EMITTED RADIATION	1ed8ac8d-3a66-4b86-be30-a5b79b3806d2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ATMOSPHERIC EMITTED RADIATION	1
5222	110	ATMOSPHERIC HEATING	06a24fd2-38b6-4a4a-a0cf-1abf149283e2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ATMOSPHERIC HEATING	1
5223	110	EMISSIVITY	49c8770a-2eb7-40f1-aab0-9c12d3aed031	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > EMISSIVITY	1
5224	110	HEAT FLUX	46a3c823-727d-4c3c-b09d-e3e3fcaa43a5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > HEAT FLUX	1
5225	110	INCOMING SOLAR RADIATION	6b3be650-6625-40b5-9b40-9e7c8a9fd336	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > INCOMING SOLAR RADIATION	1
5226	110	LONGWAVE RADIATION	68323795-3614-462f-8259-bd5293620799	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > LONGWAVE RADIATION	1
5227	110	NET RADIATION	50ee8910-449b-46c8-a59b-1cd76d632b44	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > NET RADIATION	1
5228	110	OPTICAL DEPTH/THICKNESS	13723b5d-1945-4e62-8672-4535ffdddb87	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > OPTICAL DEPTH/THICKNESS	1
5229	110	OUTGOING LONGWAVE RADIATION	006b1ea6-222d-4740-b220-03886d49cd81	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > OUTGOING LONGWAVE RADIATION	1
5230	110	POLARIZED REFLECTANCE	a87d6473-3a03-4bc6-aa21-6157fae96b8e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > POLARIZED REFLECTANCE	1
5231	110	RADIATIVE FLUX	107582ef-a356-4afa-a9a4-4e1d2200c134	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > RADIATIVE FLUX	1
5232	110	RADIATIVE FORCING	4fad64ce-32fe-413d-8b55-c78000d1980c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > RADIATIVE FORCING	1
5233	110	REFLECTANCE	bdfd401f-7eed-4a48-bd6f-f0c2a890594a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > REFLECTANCE	1
5234	110	SCATTERING	ec9e0b6a-1315-4569-93bc-0f1190bb8c08	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SCATTERING	1
5235	110	SHORTWAVE RADIATION	a8f5c969-34e9-4284-afb5-ff2113f5f881	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SHORTWAVE RADIATION	1
5236	110	SOLAR IRRADIANCE	de7647c9-b129-4cba-afe4-63fa9998206e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR IRRADIANCE	1
5237	110	SOLAR RADIATION	a0f3474e-9a54-4a82-97c4-43864b48df4c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR RADIATION	1
5238	110	SPECTRAL IRRADIANCE	b7a45c57-b652-469a-a3f2-8d38555bf478	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SPECTRAL IRRADIANCE	1
5239	110	SUNSHINE	86c95fdb-17b9-4224-a020-b1aacbea00fd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SUNSHINE	1
5240	110	TRANSMITTANCE	714be1d7-2012-4a98-bdd5-02bbcadf69d8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > TRANSMITTANCE	1
5241	110	ULTRAVIOLET RADIATION	90e7fd13-2da2-4ba6-9e0c-dbecdf7c2215	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > ULTRAVIOLET RADIATION	1
5290	116	LIGHTNING	f24c4f33-5b89-4e8d-8de7-296078a7f18a	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > LIGHTNING	1
5242	111	ATMOSPHERIC STABILITY	ff5d5c12-74d9-435d-9164-1c9d69f967d7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC STABILITY	1
5243	111	ATMOSPHERIC TEMPERATURE INDICES	25d73bcf-c8d4-4c0e-ac98-8f3e98677e73	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES	1
5244	111	SURFACE TEMPERATURE	5a7bb095-4d12-4232-bc75-b8e82197cb92	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE	1
5245	111	UPPER AIR TEMPERATURE	926c1b80-6c11-40eb-ae7f-f5bcfdc43fac	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE	1
5246	112	WATER VAPOR INDICATORS	005d192a-95b9-4fc2-afed-f87da3c3dc33	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS	1
5247	112	WATER VAPOR INDICES	4f58cf68-0d44-424a-88af-65c3edfd0945	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICES	1
5248	112	WATER VAPOR PROCESSES	3c4fe00c-6fb1-403e-a053-3a0174a6dfe6	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES	1
5249	112	WATER VAPOR PROFILES	acc824e7-8eea-4e7d-aa3d-757cda7e6ec9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROFILES	1
5250	113	LOCAL WINDS	1488b98d-6497-48b9-88db-6ee82a2e3ed3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS	1
5251	113	SURFACE WINDS	10685919-bc01-43e7-901a-b62ac44627f3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS	1
5252	113	UPPER LEVEL WINDS	592d49c4-e8ae-4ab4-bf24-ae4a896d0637	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS	1
5253	113	WIND DYNAMICS	492ffe26-8fbe-4d7d-a537-495fb96bdcce	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS	1
5254	113	WIND INDICES	25775905-dac3-4834-b709-f38a0a03b258	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND INDICES	1
5255	113	WIND PROFILES	dcc6cbbf-23a0-4ae7-bfbd-6207d35c741f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND PROFILES	1
5256	114	CLOUD DROPLET DISTRIBUTION	cbb0d517-462a-46fe-a0e6-32555f7e7f23	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DROPLET DISTRIBUTION	1
5257	114	CLOUD DYNAMICS	62019831-aaba-4d63-a5cd-73138ccfa5d0	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS	1
5258	114	CLOUD MICROPHYSICS	0cfcbaa7-727b-4199-8cca-93824b427e9b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS	1
5259	114	CLOUD PROPERTIES	c9e429cb-eff0-4dd3-9eca-527e0081f65c	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES	1
5260	114	CLOUD RADIATIVE TRANSFER	3487d350-a5a5-43d9-a60d-c1407dd2f0ce	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER	1
5261	114	CLOUD TYPES	29b61359-ebec-42c2-be05-2d7be2275954	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD TYPES	1
5262	114	CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED)	9a802ef3-680d-4bc6-a42e-aa84d5eb9908	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED)	1
5263	114	MESOSPHERIC CLOUDS (OBSERVED/ANALYZED)	04bc6942-12e0-413f-94d2-1ba7f5edf595	EARTH SCIENCE > ATMOSPHERE > CLOUDS > MESOSPHERIC CLOUDS (OBSERVED/ANALYZED)	1
5264	114	STRATOSPHERIC CLOUDS (OBSERVED/ANALYZED)	d6ab88c0-5a97-4f5e-8e4c-1c6fc6ed368f	EARTH SCIENCE > ATMOSPHERE > CLOUDS > STRATOSPHERIC CLOUDS (OBSERVED/ANALYZED)	1
5265	114	TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED)	705cd3a0-ea07-40c8-bfa1-9c26f22d13ba	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED)	1
5266	114	TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED)	20365b0a-f8df-437a-8b31-25557f7b4d82	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED)	1
5267	114	TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED)	a413f88b-859c-4035-a45b-2faa9934156b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED)	1
5268	115	ACCUMULATIVE CONVECTIVE PRECIPITATION	2b3dc817-9238-482a-8c10-d34375f3d27d	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ACCUMULATIVE CONVECTIVE PRECIPITATION	1
5269	115	ATMOSPHERIC PRECIPITATION INDICES	c7477201-761f-4cd1-b986-3e99a0be866b	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ATMOSPHERIC PRECIPITATION INDICES	1
5270	115	DROPLET SIZE	6eaed241-db16-4a1a-a06c-893da5d98b45	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > DROPLET SIZE	1
5271	115	HYDROMETEORS	56f2cdbd-2a91-4267-97eb-1680e8582322	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > HYDROMETEORS	1
5272	115	LIQUID PRECIPITATION	7d45f108-dda2-4341-b853-ee3a490aad59	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION	1
5273	115	LIQUID WATER EQUIVALENT	eca0080c-b001-4b6a-b978-f76415e28421	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID WATER EQUIVALENT	1
5274	115	PRECIPITATION AMOUNT	cad5c02a-e771-434e-bef6-8dced38a68e8	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT	1
5275	115	PRECIPITATION ANOMALIES	22a4ddef-90f0-4935-a13d-26b14723a956	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION ANOMALIES	1
5276	115	PRECIPITATION PROFILES	d4449cf4-8d4e-4282-b84d-5098715389dd	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION PROFILES	1
5277	115	PRECIPITATION RATE	ac50c468-df2f-429c-8394-9d63efcc6f9d	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION RATE	1
5278	115	SNOW WATER EQUIVALENT	30bd3a01-8cb0-4045-a998-582adbf97df9	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SNOW WATER EQUIVALENT	1
5279	115	SOLID PRECIPITATION	1906bb87-db16-46db-b814-e0b322356125	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION	1
5280	115	TOTAL SURFACE PRECIPITATION RATE	9466020a-db25-40ba-a76f-4720800efc92	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > TOTAL SURFACE PRECIPITATION RATE	1
5281	115	VIRGA	e96f2d1a-432e-44e4-bc88-6f8f35ae88fb	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > VIRGA	1
5282	116	COLD WAVE	03bc515c-af45-4a15-b2a2-65270f0e72bd	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > COLD WAVE	1
5283	116	DROUGHTS	12a896f3-993d-49f6-aafc-17378ffa3998	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > DROUGHTS	1
5284	116	EXTRATROPICAL CYCLONES	da436e9b-60e5-4a5f-a50a-08794d62bca8	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > EXTRATROPICAL CYCLONES	1
5285	116	FOG	a5ad4f63-7483-4f07-86c7-57037e5faf6c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FOG	1
5286	116	FREEZE/FROST	4539272a-f041-4fc6-883d-4c4c5bef1683	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST	1
5287	116	HAIL STORMS	a2ea1792-c011-4c7c-95c7-3bd648b1b57b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > HAIL STORMS	1
5288	116	HEAT WAVE	ca820557-401e-4e5e-ac32-29fdbc0628b3	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > HEAT WAVE	1
5289	116	ICE STORMS	5ce75010-ec8a-4af7-9e34-3e49ef2fe10c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > ICE STORMS	1
5291	116	MONSOONS	a6212424-1146-4a79-a14c-8ce88543b08b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > MONSOONS	1
5292	116	RAIN STORMS	f6b314db-883a-4493-9140-b6afda949710	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > RAIN STORMS	1
5293	116	SNOW STORMS	bc9215ae-58ec-481e-ba83-89376a298000	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SNOW STORMS	1
5294	116	SUBTROPICAL CYCLONES	edfe982b-a5bb-4001-83fa-f46f90f69b79	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES	1
5295	116	Stability/Severe Weather Indices	7844ae66-f542-442f-8359-05014bc19831	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices	1
5296	116	TORNADOES	a200e677-384a-42d6-8519-1c7735f0adb9	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES	1
5297	116	TROPICAL CYCLONES	06180441-d4bb-4fed-b36a-9b3cb2cac0fe	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES	1
5298	116	WIND STORMS	c40071d2-6478-4edf-80bb-95c3886533b9	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > WIND STORMS	1
5299	117	ACORN WORMS	70c0b882-3d34-4e2d-90bf-339ade328ee0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ACORN WORMS	1
5300	117	ARROW WORMS	328d3442-34a0-496b-ae4d-87eb447058b8	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARROW WORMS	1
5301	117	ARTHROPODS	bb87baf5-3844-4a56-865f-ea5ed420db06	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS	1
5302	117	BRYOZOANS/MOSS ANIMALS	b560f23d-f190-4c41-8bd9-4650a83296af	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > BRYOZOANS/MOSS ANIMALS	1
5303	117	BURROWS/SPOON WORMS	f70d3181-c6b6-40ec-a583-6c9e44e1c4ad	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > BURROWS/SPOON WORMS	1
5304	117	CNIDARIANS	b6164a29-8e14-4861-a30c-fefce375e284	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS	1
5305	117	COMB JELLIES	acce07bc-4e22-48b8-8396-10628c13124f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > COMB JELLIES	1
5306	117	ECHINODERMS	70892c25-4206-4673-9504-2876927d19a3	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ECHINODERMS	1
5307	117	ENTOPROCTS	23193921-88ee-4ff2-b9ca-d4688aa4bda7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ENTOPROCTS	1
5308	117	FLATWORMS/FLUKES/TAPEWORMS	8ce4bad9-f050-4b0c-845e-5e7569b6a2d2	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > FLATWORMS/FLUKES/TAPEWORMS	1
5309	117	GNATHOSTOMULIDS	e05fac08-e3de-4f41-a3fa-29d322a99ac2	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > GNATHOSTOMULIDS	1
5310	117	HORSEHAIR WORMS	e3425c65-ead7-4bf6-942c-7176a1469b58	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > HORSEHAIR WORMS	1
5311	117	LAMP SHELLS	28ae9814-61c2-4ca4-8bc5-d093c1ce5e83	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > LAMP SHELLS	1
5312	117	LORICIFERANS	470b8420-2a72-4a0c-9c87-e85c57bf01bb	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > LORICIFERANS	1
5313	117	MOLLUSKS	d85c386f-e4f7-4e1c-a16e-34dbb12bb2be	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS	1
5314	117	PEANUT WORMS	3d179cd8-3d64-47a8-b665-ac1382053aff	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > PEANUT WORMS	1
5315	117	PHORONIDS	bb62f1cf-a6e5-4d9d-a3ab-c665b93ce072	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > PHORONIDS	1
5316	117	PRIAPULANS	9c974992-0ec2-4c55-9ab9-e8158f446fe7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > PRIAPULANS	1
5317	117	RIBBON WORMS	0b5fd1dc-cfff-4bd8-9807-b5dd5ecf83fe	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > RIBBON WORMS	1
5318	117	ROTIFERS	6b3f96de-62f8-482a-87a5-6efcc3414af7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ROTIFERS	1
5319	117	ROUNDWORMS	2c1cf609-c70d-4811-8514-3ca45a8bb380	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ROUNDWORMS	1
5320	117	SEGMENTED WORMS (ANNELIDS)	ab1952ae-de34-4299-ad10-9c9b2baf87f5	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SEGMENTED WORMS (ANNELIDS)	1
5321	117	SPINY-HEADED WORMS	af9520f0-6011-45e0-a1d8-bd8c3ed042b0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SPINY-HEADED WORMS	1
5322	117	SPONGES	bfbfd84c-6bf0-412f-9e75-1bad5241c339	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SPONGES	1
5323	117	TUNICATES	c34af039-4868-41f0-aaf0-39e8e9554e03	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > TUNICATES	1
5324	117	WATER BEARS (TARDIGRADES)	fb4834d9-7bfe-4283-86f7-931532baa79c	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > WATER BEARS (TARDIGRADES)	1
5325	117	WHEEL WEAVERS (CYCLIOPHORANS)	fa4b61fa-32e7-420f-988f-df5527b6f935	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > WHEEL WEAVERS (CYCLIOPHORANS)	1
5326	118	AMPHIBIANS	a27837ae-62f7-4931-9da1-0bf63f4755fc	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > AMPHIBIANS	1
5327	118	BIRDS	1bf8f27a-d6ff-4cb6-acb7-7e5cce11e029	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS	1
5328	118	FISH	ea855d4c-f132-44f9-b31c-447e1101684d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH	1
5329	118	MAMMALS	f5161094-3593-4bc1-85ea-c8c2ecab1d9a	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS	1
5330	118	REPTILES	5d3725b6-743b-4dda-bb54-b64f201ec4d1	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > REPTILES	1
5331	119	CYANOBACTERIA (BLUE-GREEN ALGAE)	166de4c9-89ad-4248-b771-512beb1705cf	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > BACTERIA/ARCHAEA > CYANOBACTERIA (BLUE-GREEN ALGAE)	1
5332	120	LICHENS	e85b6d64-a230-4c1d-99a5-c62be8af18c7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > FUNGI > LICHENS	1
5333	120	MUSHROOMS	14fa5360-320c-4d54-9bf6-9871a4b308d7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > FUNGI > MUSHROOMS	1
5334	120	SLIME MOLDS	05763c43-c6ed-4071-b868-2ea6c1335c12	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > FUNGI > SLIME MOLDS	1
5335	120	YEASTS/TRUFFLES	ee2e5028-1963-4de1-a883-b9e546d682a4	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > FUNGI > YEASTS/TRUFFLES	1
5336	121	ANGIOSPERMS (FLOWERING PLANTS)	5eda068f-97ea-474a-8a1b-b193f6901251	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > ANGIOSPERMS (FLOWERING PLANTS)	1
5337	121	FERNS AND ALLIES	589875d3-4770-4fb3-871c-b37c7aff4b47	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > FERNS AND ALLIES	1
5338	121	GYMNOSPERMS	566e22da-d72e-4663-89d2-ced5aea948ea	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > GYMNOSPERMS	1
5339	121	MACROALGAE (SEAWEEDS)	e731c2a1-e4b0-42e9-bed9-bd911c9b496c	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MACROALGAE (SEAWEEDS)	1
5340	121	MICROALGAE	d3594523-ba0d-4275-b121-95039f905058	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE	1
5341	121	MOSSES/HORNWORTS/LIVERWORTS	934bd870-ffa8-41d8-8da9-214b73707168	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MOSSES/HORNWORTS/LIVERWORTS	1
5342	122	AMOEBOIDS	663a2ea2-e2bf-4209-ae9b-334c8222b106	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > AMOEBOIDS	1
5343	122	CILIATES	6f2a1cfb-13f4-444f-a6e6-2d8b29797253	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > CILIATES	1
5344	122	DIATOMS	fdb04105-e8ba-4a83-9c35-ed3c931ccc9f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > DIATOMS	1
5345	122	FLAGELLATES	2095acb5-14af-40fe-af22-e6af2e3528b5	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > FLAGELLATES	1
5346	122	MACROALGAE (SEAWEEDS)	81655dc5-83d3-4daf-81c8-dc1522e9906e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > MACROALGAE (SEAWEEDS)	1
5347	122	PLANKTON	a69dd814-e7c0-437f-ba2a-63500f68c9a3	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > PLANKTON	1
5348	122	SLIME MOLDS	98b35c6b-5d40-41d0-b29f-a6b159c03b78	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > SLIME MOLDS	1
5349	122	SPOROZOANS	32ffe87f-c0f0-4398-9a6a-755d7f87a5ff	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > SPOROZOANS	1
5350	124	COMMUNITY DYNAMICS	8fb66b46-b998-4412-a541-d2acabdf484b	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS	1
5351	124	ECOSYSTEM FUNCTIONS	233a4d81-44f8-4b0e-8ad3-695f641729f8	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS	1
5352	124	ECOTOXICOLOGY	dd539b52-6de1-4b1b-a60c-fa5782f4d64b	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOTOXICOLOGY	1
5353	124	FIRE ECOLOGY	62c6d256-e6d4-4204-b7a8-e084dd52d30a	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > FIRE ECOLOGY	1
5354	124	SPECIES/POPULATION INTERACTIONS	58f39353-7e1c-4884-9501-376cd0377fbf	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS	1
5355	125	ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS	c4a619e9-88ba-4dc6-91a6-5f95284d6f80	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS	1
5356	125	AQUATIC ECOSYSTEMS	c6455081-132d-4661-bb5f-22edf2f90800	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS	1
5357	125	FRESHWATER ECOSYSTEMS	ad73e951-fb5b-4a0b-b034-9469a8bfccaa	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS	1
5358	125	MARINE ECOSYSTEMS	f6350232-b1c7-458c-bc43-bda357ebb6db	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS	1
5359	125	TERRESTRIAL ECOSYSTEMS	9361962c-cfc7-4428-8843-b3502718c382	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS	1
5360	126	AFFORESTATION/REFORESTATION	a28eeef3-b252-4309-957b-860d2e0f97ef	EARTH SCIENCE > BIOSPHERE > VEGETATION > AFFORESTATION/REFORESTATION	1
5361	126	BIOMASS	686feba9-87ba-474c-8280-7f67565cfb2f	EARTH SCIENCE > BIOSPHERE > VEGETATION > BIOMASS	1
5362	126	CANOPY CHARACTERISTICS	abbba948-9b77-4e19-a855-49a7fbc17696	EARTH SCIENCE > BIOSPHERE > VEGETATION > CANOPY CHARACTERISTICS	1
5363	126	CANOPY TRANSMITTANCE	2edf648a-6a71-44c3-9c1a-8fcdd2dcc61c	EARTH SCIENCE > BIOSPHERE > VEGETATION > CANOPY TRANSMITTANCE	1
5364	126	CARBON	6f6537f5-773f-4df1-862b-d9ab80eb5e04	EARTH SCIENCE > BIOSPHERE > VEGETATION > CARBON	1
5365	126	CROWN	c59b0666-e20f-4134-847b-89719ed5621a	EARTH SCIENCE > BIOSPHERE > VEGETATION > CROWN	1
5366	126	DECIDUOUS VEGETATION	b7de16ed-c090-449b-81c1-44fe5b1195f0	EARTH SCIENCE > BIOSPHERE > VEGETATION > DECIDUOUS VEGETATION	1
5367	126	DOMINANT SPECIES	df597f06-8575-4726-acac-65b2bd432d59	EARTH SCIENCE > BIOSPHERE > VEGETATION > DOMINANT SPECIES	1
5368	126	EVERGREEN VEGETATION	16a7b4d6-e47f-4753-8803-f72edc4e1c5e	EARTH SCIENCE > BIOSPHERE > VEGETATION > EVERGREEN VEGETATION	1
5369	126	EXOTIC VEGETATION	f717330e-3656-4910-beed-d54cc9a19c2b	EARTH SCIENCE > BIOSPHERE > VEGETATION > EXOTIC VEGETATION	1
5370	126	FOREST COMPOSITION/VEGETATION STRUCTURE	a8d3f9a0-be0b-4690-86b9-ac64d951886a	EARTH SCIENCE > BIOSPHERE > VEGETATION > FOREST COMPOSITION/VEGETATION STRUCTURE	1
5371	126	HERBIVORY	40766d01-bda1-420b-9fd1-fba6d6924f3f	EARTH SCIENCE > BIOSPHERE > VEGETATION > HERBIVORY	1
5372	126	IMPORTANCE VALUE	536a5a5a-28bb-473a-aa95-6d2dd1e5098d	EARTH SCIENCE > BIOSPHERE > VEGETATION > IMPORTANCE VALUE	1
5373	126	INDIGENOUS VEGETATION	0bfb8ae4-c08a-4d69-82d2-1b1b0d4acef6	EARTH SCIENCE > BIOSPHERE > VEGETATION > INDIGENOUS VEGETATION	1
5374	126	LEAF CHARACTERISTICS	bca1b724-3370-4a26-bcbc-3530ce4ddc97	EARTH SCIENCE > BIOSPHERE > VEGETATION > LEAF CHARACTERISTICS	1
5375	126	LITTER CHARACTERISTICS	afc54d28-de94-4674-9528-39f00bf74d6d	EARTH SCIENCE > BIOSPHERE > VEGETATION > LITTER CHARACTERISTICS	1
5376	126	MACROPHYTES	bf0ddf9c-39ba-4b2d-91ac-63021d644276	EARTH SCIENCE > BIOSPHERE > VEGETATION > MACROPHYTES	1
5377	126	NITROGEN	ed7c506e-b18e-4a93-ac03-4bdfe119b72f	EARTH SCIENCE > BIOSPHERE > VEGETATION > NITROGEN	1
5378	126	NUTRIENTS	9bcb805c-718e-42c3-913d-174bdf06d4c1	EARTH SCIENCE > BIOSPHERE > VEGETATION > NUTRIENTS	1
5379	126	PHOSPHORUS	47f4e7ac-b4ca-4ef9-824b-a36ea5510526	EARTH SCIENCE > BIOSPHERE > VEGETATION > PHOSPHORUS	1
5380	126	PHOTOSYNTHETICALLY ACTIVE RADIATION	db69ecb1-0738-4d82-943f-ae92093f500d	EARTH SCIENCE > BIOSPHERE > VEGETATION > PHOTOSYNTHETICALLY ACTIVE RADIATION	1
5381	126	PIGMENTS	3e801e91-897e-4528-8f4c-4ec527ad33cc	EARTH SCIENCE > BIOSPHERE > VEGETATION > PIGMENTS	1
5382	126	PLANT CHARACTERISTICS	0408bac9-c247-4b00-80de-f4665b813658	EARTH SCIENCE > BIOSPHERE > VEGETATION > PLANT CHARACTERISTICS	1
5383	126	PLANT PHENOLOGY	3f45aadf-ec7c-43a1-a008-b24ca139837a	EARTH SCIENCE > BIOSPHERE > VEGETATION > PLANT PHENOLOGY	1
5385	126	RECLAMATION/REVEGETATION/RESTORATION	86dfb9ca-6587-4a91-b397-f220bb48a1eb	EARTH SCIENCE > BIOSPHERE > VEGETATION > RECLAMATION/REVEGETATION/RESTORATION	1
5386	126	REFORESTATION	fe6b37b9-f95a-491e-a58e-22aa66be9a9d	EARTH SCIENCE > BIOSPHERE > VEGETATION > REFORESTATION	1
5387	126	TREE RINGS	0e06e528-e796-4b7c-9878-dbcb061d878d	EARTH SCIENCE > BIOSPHERE > VEGETATION > TREE RINGS	1
5388	126	VEGETATION COVER	5bdb3251-4811-439c-b172-9bbcd98e84b3	EARTH SCIENCE > BIOSPHERE > VEGETATION > VEGETATION COVER	1
5389	126	VEGETATION INDEX	b7812c71-4b9e-4016-b4ba-dfcdb7e62365	EARTH SCIENCE > BIOSPHERE > VEGETATION > VEGETATION INDEX	1
5390	126	VEGETATION SPECIES	de0ace5c-fa2b-47ca-93db-79d8df7ab6f2	EARTH SCIENCE > BIOSPHERE > VEGETATION > VEGETATION SPECIES	1
5391	127	CLOUD INDICATORS	8c4e2397-aed6-4ce4-9ead-08323e2f90ae	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > CLOUD INDICATORS	1
5392	127	COMPOUND EXTREME EVENTS	83e9ddee-5887-4758-a3ba-5cb17a7d4ed5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > COMPOUND EXTREME EVENTS	1
5393	127	EXTREME WEATHER	b29b46ad-f05f-4144-b965-5f606ce96963	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER	1
5394	127	FRESH WATER RIVER DISCHARGE	12dc1f4f-2116-4b74-a1bd-bc61e8e57a5b	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > FRESH WATER RIVER DISCHARGE	1
5395	127	HUMIDITY INDICES	b881cf8f-7260-4980-80bc-4b6ae3716c39	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES	1
5396	127	OCEAN OVERTURNING	dbf8a0cf-1e9b-4bc4-95a2-819bb16af00c	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > OCEAN OVERTURNING	1
5397	127	OCEAN UPWELLING INDICES	7d3e2368-75ba-43b9-bdce-bba2ff8d3e2c	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > OCEAN UPWELLING INDICES	1
5398	127	OCEAN UPWELLING/DOWNWELLING	873ed434-9407-4fd8-9660-41e50b0eb786	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > OCEAN UPWELLING/DOWNWELLING	1
5399	127	PRECIPITATION INDICATORS	789939a6-3cd5-46f3-bdfd-5cdd6a012500	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICATORS	1
5400	127	PRECIPITATION INDICES	52347642-9786-4b59-be77-02e9f307118d	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICES	1
5401	127	SEA LEVEL RISE	536a86bd-3dd1-4f4a-9b4a-222a12746db5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA LEVEL RISE	1
5402	127	SEA SURFACE TEMPERATURE INDICES	b83895e9-bac8-49fe-bcf5-8fe4d8fcaa16	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES	1
5403	127	SURFACE SALINITY	1d8525f0-0cfc-4d59-8677-da5c8038deb7	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SURFACE SALINITY	1
5404	130	SEA ICE CONCENTRATION	1c0ebf89-f115-4e0d-9942-8ff8289bd330	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SEA ICE CONCENTRATION	1
5405	127	TELECONNECTIONS	b887d3e5-4280-43d2-a34e-0f63ac086b6a	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS	1
5406	130	SEA ICE ELEVATION	5d5cf73b-f833-4f8d-84a1-8a3840f3b4af	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SEA ICE ELEVATION	1
5407	127	TEMPERATURE INDICATORS	2dcffd8f-2b01-4c68-a4f2-c4940d2709a3	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS	1
5408	127	TEMPERATURE INDICES	e8580cbb-701a-4ab1-a40f-5fae4ae1ea24	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES	1
5409	128	BIRTH RATE DECLINE/INCREASE	379dd4c3-04d7-4f76-9bb9-83d0b8e1a2aa	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > BIRTH RATE DECLINE/INCREASE	1
5410	128	BREEDING PRODUCTIVITY	0a07badb-1382-4f63-8344-7ba063b05534	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > BREEDING PRODUCTIVITY	1
5411	128	CANOPY TEMPERATURE VARIABILITY	9a40bc0e-aece-4b4a-a87d-4869c8b903f8	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > CANOPY TEMPERATURE VARIABILITY	1
5412	128	HYPOXIC CONDITIONS	853c3456-5397-4e16-ba67-51e4f4205db5	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > HYPOXIC CONDITIONS	1
5413	128	INDICATOR SPECIES	6448f172-1560-4ea7-8826-8ac85dc820f3	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > INDICATOR SPECIES	1
5414	128	INVASIVE SPECIES	93c8b32d-ab89-43e1-b58c-f1823fa7d118	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > INVASIVE SPECIES	1
5415	128	PHENOLOGICAL CHANGES	cc5ab64b-11d0-4196-b7b3-f9c61e5e3ac6	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > PHENOLOGICAL CHANGES	1
5416	128	RANGE CHANGES	f5c63c23-f819-46e8-bc97-1e894424c00c	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > RANGE CHANGES	1
5417	128	SPECIES MIGRATION	0de668aa-cc97-482d-a0eb-cddcb1a705b6	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > SPECIES MIGRATION	1
5418	128	VECTOR SPECIES	1d9f0eb8-7233-4969-b40c-979d601ebaa7	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > VECTOR SPECIES	1
5419	129	ATMOSPHERIC FEEDBACKS	fc77777e-614f-41f1-9b97-d5324fa99105	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS > ATMOSPHERIC FEEDBACKS	1
5420	129	COUPLED SYSTEM FEEDBACKS	6a6bed83-f95a-44e6-8ae0-1371b532abc3	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS > COUPLED SYSTEM FEEDBACKS	1
5421	129	CRYOSPHERIC FEEDBACKS	3da6855e-9be8-4a79-826e-4ce984ed49a5	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS > CRYOSPHERIC FEEDBACKS	1
5422	129	LAND SURFACE FEEDBACKS	514c891b-60b8-4a6f-adb3-0366c75588e9	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS > LAND SURFACE FEEDBACKS	1
5423	129	OCEANIC FEEDBACKS	80d337f4-8e90-456a-9a5b-33e5f5c907ce	EARTH SCIENCE > CLIMATE INDICATORS > CLIMATE FEEDBACKS > OCEANIC FEEDBACKS	1
5424	130	AVALANCHE	bb8c48bc-a36e-4f7e-afda-3244b058bc9c	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > AVALANCHE	1
5425	130	DEPTH HOAR	82f49e65-c032-4f74-b5c2-a3f8058b7a71	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > DEPTH HOAR	1
5426	130	FIRN LIMIT	9fec9f47-c45d-4f15-8be5-d71424f33647	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > FIRN LIMIT	1
5427	130	GLACIAL MEASUREMENTS	2d79af4f-d15f-40cc-b0bf-8f5c8eb1fce5	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS	1
5428	130	ICE DEPTH/THICKNESS	fadd59e2-e1d2-44f6-9e41-0589eb953198	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > ICE DEPTH/THICKNESS	1
5429	130	ICE EDGES	f4c1a555-4758-47ce-baa6-536730333833	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > ICE EDGES	1
5430	130	ICE EXTENT	50f0cf56-c119-4ac1-9a88-8eb04fa666ad	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > ICE EXTENT	1
5431	130	ICE FLOES	4733ef2c-e512-451b-8079-78ff7278e35c	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > ICE FLOES	1
5432	130	ICE GROWTH/MELT	0ff2a38d-00f6-459d-ac9a-9a983bda602e	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > ICE GROWTH/MELT	1
5477	136	CRYOSOLS	0cd7a96f-46e1-4d86-93d0-9cbb6fda61e3	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > CRYOSOLS	1
5433	130	RIVER ICE DEPTH/EXTENT	fde8a54a-8aaa-45fd-bb66-3105e4c57102	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > RIVER ICE DEPTH/EXTENT	1
5434	130	SALINITY	ee0fce70-2097-4f5b-853a-c34e6cbff929	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SALINITY	1
5435	130	SNOW COVER	8ef6560e-c699-49b4-bcb3-6db68506ca22	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SNOW COVER	1
5436	130	SNOW DEPTH	008708ac-65a4-481a-8e03-640376f42f56	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SNOW DEPTH	1
5437	130	SNOW ENERGY BALANCE	29f386e9-84fb-4e5d-9733-20233c63b1be	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SNOW ENERGY BALANCE	1
5438	130	SNOW MELT	b1be402f-336c-4f1f-8542-9807264a09a7	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > SNOW MELT	1
5439	131	FIJI INDEX	47200796-7541-4659-acf4-32b5303bcc1f	EARTH SCIENCE > CLIMATE INDICATORS > ENVIRONMENTAL VULNERABILITY INDEX (EVI) > FIJI INDEX	1
5440	131	SAMOA INDEX	2c1e046e-2feb-4cb7-a6dd-f3753db7b5f5	EARTH SCIENCE > CLIMATE INDICATORS > ENVIRONMENTAL VULNERABILITY INDEX (EVI) > SAMOA INDEX	1
5441	131	TUVALU INDEX	585182e9-6e5b-4ad6-96fe-065ffd31f7e8	EARTH SCIENCE > CLIMATE INDICATORS > ENVIRONMENTAL VULNERABILITY INDEX (EVI) > TUVALU INDEX	1
5442	132	DROUGHT INDICES	f50672b3-13d8-4206-b6c9-a1f9891ea470	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > DROUGHT INDICES	1
5443	132	EROSION	b51f738c-7061-4ced-b216-53734ce4cb43	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > EROSION	1
5444	132	FIRE WEATHER INDEX	7c1977bc-dfe7-4761-9b30-f42ec986d360	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > FIRE WEATHER INDEX	1
5445	132	FOREST FIRE DANGER INDEX	16329a9b-72ea-4b46-b507-2ce389c63f50	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > FOREST FIRE DANGER INDEX	1
5446	132	LANDSLIDES	36bdce45-37df-4475-9eed-73469a594edb	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LANDSLIDES	1
5447	132	LENGTH OF GROWING SEASON	ed8797be-661a-48c9-a7fe-2600b6c7c067	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LENGTH OF GROWING SEASON	1
5448	132	SATELLITE SOIL MOISTURE INDEX	32e1b1ec-fa69-47b5-b0d6-d71948e3997a	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > SATELLITE SOIL MOISTURE INDEX	1
5449	132	SOIL EROSION	cb21c5cb-cc49-4328-a72d-94ccca1fa888	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > SOIL EROSION	1
5450	132	SOIL MOISTURE	27dd85c2-3403-438d-8b0c-8d424df60468	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > SOIL MOISTURE	1
5451	132	SOIL TEMPERATURE	b29ee2f4-b2ce-4b19-b8e3-2d74d071549b	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > SOIL TEMPERATURE	1
5452	132	SURFACE MOISTURE INDEX	c7503ec5-4e63-446a-9390-72c8a638a0af	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > SURFACE MOISTURE INDEX	1
5453	132	TREE LINE SHIFT	d11df264-e70d-456c-9223-07f34e80b352	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > TREE LINE SHIFT	1
5454	132	VEGETATION COVER	8d1157c4-d36b-40db-aa82-3603716f9988	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > VEGETATION COVER	1
5455	133	ALUMINUM-26 ANALYSIS	1efdd374-40a1-4118-a1da-61c647017ec9	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ALUMINUM-26 ANALYSIS	1
5456	133	BERYLLIUM-10 ANALYSIS	4bd6aafb-9240-4006-ada3-4b6a0501b612	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BERYLLIUM-10 ANALYSIS	1
5457	133	BIOLOGICAL RECORDS	5553fe9d-ab0a-4305-86a6-1f7f697e15e4	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS	1
5458	133	ICE CORE RECORDS	08a4f002-f368-414d-b923-83dd498452d8	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS	1
5459	133	LAND RECORDS	2bedb6b3-6e92-42e2-b382-60e2a6aab8e9	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS	1
5460	133	MASS EXTINCTIONS	703d0c14-1978-4e7f-a51a-233c695823b9	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > MASS EXTINCTIONS	1
5461	133	OCEAN/LAKE RECORDS	5237fae3-c98e-4d4a-9013-d7c824b3862b	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS	1
5462	133	OXYGEN ISOTOPE ANALYSIS	2f2d4df2-0701-4fe1-9d9b-e7e1c8678a8f	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OXYGEN ISOTOPE ANALYSIS	1
5463	133	PALEOCLIMATE FORCING	dc3f297b-8471-4101-b70e-dc5765762061	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE FORCING	1
5464	133	PALEOCLIMATE RECONSTRUCTIONS	6f6423e8-ab4e-4572-8982-d9c40f64e28b	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS	1
5465	133	PERMAFROST/METHANE RELEASE	478092f3-7cdd-4136-84ec-cebf0d539480	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PERMAFROST/METHANE RELEASE	1
5466	133	PLATE TECTONICS	6971fecc-af14-4c97-82db-2b01c98453b9	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PLATE TECTONICS	1
5467	133	SPELEOTHEMS	1cbefa2a-484e-4742-ad3d-d347d27272bd	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > SPELEOTHEMS	1
5468	133	VOLCANIC ACTIVITY	08bc1b7d-b27b-43e2-a728-4939efb88f08	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > VOLCANIC ACTIVITY	1
5469	134	SUNSPOT ACTIVITY	3429bc72-0780-44c8-9743-92f84118279d	EARTH SCIENCE > CLIMATE INDICATORS > SUN-EARTH INTERACTIONS > SUNSPOT ACTIVITY	1
5470	135	FRESHWATER RUNOFF	915399a1-eb5b-475b-ae9a-ff45f1dcddc9	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > FRESHWATER RUNOFF	1
5471	135	MOUNTAIN SNOW LINE SHIFT	56e7e412-b354-4ef4-8742-f1f5681c378a	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > MOUNTAIN SNOW LINE SHIFT	1
5472	135	PERMAFROST MELT	ed0501c5-310c-42ab-b1eb-66e211f22803	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > PERMAFROST MELT	1
5473	135	RIVER/LAKE ICE BREAKUP	64baed75-e3c0-4495-9bc9-c5b9373670f6	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > RIVER/LAKE ICE BREAKUP	1
5474	135	RIVER/LAKE ICE FREEZE	2adde197-3f0f-4eda-ae00-a337dfa853c3	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > RIVER/LAKE ICE FREEZE	1
5475	135	SNOW COVER DEGRADATION	994cc55d-b789-4f03-98dc-4cd0f58ad12a	EARTH SCIENCE > CLIMATE INDICATORS > TERRESTRIAL HYDROSPHERE INDICATORS > SNOW COVER DEGRADATION	1
5476	136	ACTIVE LAYER	2e544263-d92f-46c2-9568-25e36d0b9825	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > ACTIVE LAYER	1
5478	136	GROUND ICE	4931dcac-8b89-4bc9-ba59-469cfdcf6f12	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > GROUND ICE	1
5479	136	PERIGLACIAL PROCESSES	097a0fad-d822-49ad-bd12-232e9ea7cb30	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > PERIGLACIAL PROCESSES	1
5480	136	PERMAFROST	c82f3480-545f-4491-83f1-0477369ddcd8	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > PERMAFROST	1
5481	136	ROCK GLACIERS	b1ce822a-139b-4e11-8bbe-453f19501c36	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > ROCK GLACIERS	1
5482	136	SEASONALLY FROZEN GROUND	2a109b2f-947a-4c2c-9db9-ae315a53ef93	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > SEASONALLY FROZEN GROUND	1
5483	136	SOIL TEMPERATURE	021714ad-1cae-441c-bb6f-4be866a0f742	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > SOIL TEMPERATURE	1
5484	136	TALIK	78e5e44c-7832-456d-a599-893ea87ae695	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > TALIK	1
5485	137	ABLATION ZONES/ACCUMULATION ZONES	95fbaefd-1afe-4887-a1ba-fc338a8109bb	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ABLATION ZONES/ACCUMULATION ZONES	1
5486	137	AGE AT ICE-THICKNESS-NORMALIZED DEPTHS	ab4b800d-820f-40cc-bb01-4e8835368d04	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > AGE AT ICE-THICKNESS-NORMALIZED DEPTHS	1
5487	137	AGE OF INTERNAL REFLECTIONS	9ce536e1-06c8-4817-af5f-b625cfe571a7	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > AGE OF INTERNAL REFLECTIONS	1
5488	137	BASAL SHEAR STRESS	68d0f29d-cf46-4f8c-8cad-83817a7093bc	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > BASAL SHEAR STRESS	1
5489	137	DEPTHS AT SPECIFIC AGES	70541b66-c911-47fb-a99a-5638a9cb55d4	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > DEPTHS AT SPECIFIC AGES	1
5490	137	FIRN	6159b9d9-4aa5-4dec-8146-0e47751449ff	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > FIRN	1
5491	137	GEOMETRY OF INTERNAL REFLECTIONS	ab319cdf-a34c-446c-9fc0-27605048364e	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GEOMETRY OF INTERNAL REFLECTIONS	1
5492	137	GLACIER ELEVATION/ICE SHEET ELEVATION	13bf19c5-087f-4fe0-87ea-ef6f7ecd5444	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER ELEVATION/ICE SHEET ELEVATION	1
5493	137	GLACIER FACIES	399a84d1-ccf5-4167-a699-15eb7d1ad1e6	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER FACIES	1
5494	137	GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	9f408faa-a427-44e9-a194-b1b9caff1e6d	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	1
5495	137	GLACIER MOTION/ICE SHEET MOTION	73f3c797-2eed-4f0d-accf-7e8a36a3fa93	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER MOTION/ICE SHEET MOTION	1
5496	137	GLACIER THICKNESS/ICE SHEET THICKNESS	5034ba1f-7208-40a1-beeb-43aefe1c0c33	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER THICKNESS/ICE SHEET THICKNESS	1
5497	137	GLACIER TOPOGRAPHY/ICE SHEET TOPOGRAPHY	bf19f1d1-ae18-4ff2-95f6-dc0ed812c568	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIER TOPOGRAPHY/ICE SHEET TOPOGRAPHY	1
5498	137	GLACIERS	68eed887-8008-4352-b420-949457ab59ab	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > GLACIERS	1
5499	137	ICE SHEETS	10b1872b-4a48-4360-a449-388e8988bca9	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ICE SHEETS	1
5500	137	ICEBERGS	4d95ccc8-3ef9-40df-85e7-db36cb815499	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ICEBERGS	1
5501	138	FREEBOARD	a4466cbe-b991-427b-97b8-fdc284b9ef21	EARTH SCIENCE > CRYOSPHERE > SEA ICE > FREEBOARD	1
5502	138	HEAT FLUX	5569b7a3-3a4b-4799-8c68-98126757074b	EARTH SCIENCE > CRYOSPHERE > SEA ICE > HEAT FLUX	1
5503	138	ICE DEFORMATION	1009557b-0d4b-4c13-81a0-fd95c15bf158	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE DEFORMATION	1
5504	138	ICE DEPTH/THICKNESS	c7708bb6-a0fa-4905-b99d-c468da7d951a	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE DEPTH/THICKNESS	1
5505	138	ICE EDGES	5fa04fa9-06c7-41c7-98f9-f92756f080ea	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE EDGES	1
5506	138	ICE EXTENT	63b37017-9d57-4247-af4e-2df36ee3ed03	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE EXTENT	1
5507	138	ICE FLOES	af0d756e-784e-4747-97d0-3425baf5d09b	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE FLOES	1
5508	138	ICE GROWTH/MELT	d9667e73-30db-45f9-861c-e0a5caaf2bf0	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE GROWTH/MELT	1
5509	138	ICE ROUGHNESS	ce3a1edd-a2fe-4efd-8971-9dd7b97b6d79	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE ROUGHNESS	1
5510	138	ICE TEMPERATURE	f6e7aa9a-ae65-480e-84fa-b3a5d523e822	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE TEMPERATURE	1
5511	138	ICE TYPES	6bfd4d52-fad4-470f-9da0-fa7df2a5b4aa	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICE TYPES	1
5512	138	ICEBERGS	1efe6ac1-d375-44c3-b8ec-d0ff2987a881	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ICEBERGS	1
5513	138	ISOTOPES	f0d4b06b-c498-4760-bc92-877e28f3a098	EARTH SCIENCE > CRYOSPHERE > SEA ICE > ISOTOPES	1
5514	138	LEADS	4f0f606c-6bf8-4b8c-9431-d5696fe8a5f2	EARTH SCIENCE > CRYOSPHERE > SEA ICE > LEADS	1
5515	138	PACK ICE	5d7ea074-225b-4221-b122-e6a085cdce24	EARTH SCIENCE > CRYOSPHERE > SEA ICE > PACK ICE	1
5516	138	POLYNYAS	70acf223-7895-4cbe-aca6-815babb2b7ed	EARTH SCIENCE > CRYOSPHERE > SEA ICE > POLYNYAS	1
5517	138	REFLECTANCE	cece77b6-42bf-44f6-9193-050cbc5f4cf7	EARTH SCIENCE > CRYOSPHERE > SEA ICE > REFLECTANCE	1
5518	138	SALINITY	6bc39a6d-cc60-467a-9181-d8b4e02a1cb0	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SALINITY	1
5519	138	SEA ICE AGE	3488309d-ef21-4d60-81a3-78fb99ffa756	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SEA ICE AGE	1
5520	138	SEA ICE CONCENTRATION	8012fda7-3ea4-4ef2-bb4e-0f66d4d9e850	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SEA ICE CONCENTRATION	1
5521	138	SEA ICE ELEVATION	139b0dae-27bb-42bd-8027-81fb9fd8f85d	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SEA ICE ELEVATION	1
5522	138	SEA ICE MOTION	1455c369-88e2-411b-83f7-c914b20609b1	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SEA ICE MOTION	1
5523	138	SNOW DEPTH	aa645419-cff3-4f5b-84af-e3de41dd0d16	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SNOW DEPTH	1
5524	138	SNOW MELT	064f9784-697e-414c-b463-29cfd734e689	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SNOW MELT	1
5525	139	ALBEDO	41ebe049-230e-4ff7-acb1-43de68ace83e	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ALBEDO	1
5526	139	AVALANCHE	e1dbe955-7285-4df2-a854-07693fce44ec	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > AVALANCHE	1
5527	139	DEPTH HOAR	c306d542-9be8-449d-ba33-28ad033c77aa	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > DEPTH HOAR	1
5528	139	FREEZE/THAW	dafb67df-dc6d-40a0-8d94-e4621d2538ce	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > FREEZE/THAW	1
5529	139	FROST	ea936862-2c98-41e5-8514-6b7288a5f941	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > FROST	1
5530	139	ICE DEPTH/THICKNESS	e28676de-738d-4112-8897-ee585b7d1d84	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE DEPTH/THICKNESS	1
5531	139	ICE EXTENT	19409c76-09d4-455c-b1f1-dc2e647f7403	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE EXTENT	1
5532	139	ICE GROWTH/MELT	19594c37-ef32-4b03-bda6-abf8a321fdb9	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE GROWTH/MELT	1
5533	139	ICE MOTION	4b85cc37-1577-43f6-8cfa-8da2c49eaece	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE MOTION	1
5534	139	ICE VELOCITY	3896f032-388f-408e-b988-bf7e100704ba	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > ICE VELOCITY	1
5535	139	LAKE ICE	8cb47594-3af6-4f4f-8ba1-4299a6d6887e	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > LAKE ICE	1
5536	139	PERMAFROST	1f4cdbc4-0f65-4384-83c9-9422c280717d	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > PERMAFROST	1
5537	139	REFLECTANCE	00a21e9c-0c1d-4931-b9fa-b0204625a98a	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > REFLECTANCE	1
5538	139	RIVER ICE	52e6600b-7a51-4267-8b62-e79034db3a48	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > RIVER ICE	1
5539	139	SNOW COVER	c8ff0035-4776-4eb9-8cc9-a63d380102c8	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW COVER	1
5540	139	SNOW DENSITY	ba2e2eff-77e0-4071-8884-b2af06e5fc7b	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW DENSITY	1
5541	139	SNOW DEPTH	47bc8942-6fdd-4173-bf38-209e933d843f	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW DEPTH	1
5542	139	SNOW ENERGY BALANCE	a3520db9-7bed-4f55-a9f6-028d52af6091	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW ENERGY BALANCE	1
5543	139	SNOW FACIES	99506fd1-5f84-485d-8e26-03e4f7b55136	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW FACIES	1
5544	139	SNOW MELT	58f98d2a-d7d6-47d4-b826-68fdc57e79bb	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW MELT	1
5545	139	SNOW MICROSTRUCTURE	4dc6b614-36ad-4e3b-ac6f-af6e0aa6378b	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW MICROSTRUCTURE	1
5546	139	SNOW STRATIGRAPHY	9e15c793-ede5-4089-8fb7-5bbb31ff7913	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW STRATIGRAPHY	1
5547	139	SNOW WATER EQUIVALENT	587e4d68-36f0-45b5-9978-4b3edd58a1c0	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW WATER EQUIVALENT	1
5548	139	SNOW/ICE CHEMISTRY	dfe4b154-84e0-4005-81ce-90daf38c06e3	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW/ICE CHEMISTRY	1
5549	139	SNOW/ICE TEMPERATURE	99bc6084-32bc-405a-b2e9-efd906fa370b	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW/ICE TEMPERATURE	1
5550	139	WHITEOUT	067004b9-1628-4c00-8bfb-28f910b68d59	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > WHITEOUT	1
5551	140	ADMINISTRATIVE DIVISIONS	1ae304de-252c-45da-8dd8-df99a281e4f4	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES > ADMINISTRATIVE DIVISIONS	1
5552	140	BOUNDARY SURVEYS	8064b11d-8f9f-4c89-94fd-8a7cba95bb64	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES > BOUNDARY SURVEYS	1
5553	140	POLITICAL DIVISIONS	3381412c-54f0-4911-85ef-81d669c896cf	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES > POLITICAL DIVISIONS	1
5554	141	AGRICULTURE PRODUCTION	83741fb9-6f86-4670-abbb-c1f3b14a939d	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > AGRICULTURE PRODUCTION	1
5555	141	AQUACULTURE PRODUCTION	392d3da2-c03c-4aa5-bf60-417984f824a6	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > AQUACULTURE PRODUCTION	1
5556	141	ENERGY PRODUCTION/USE	b73cee46-8e2c-4df9-b1ed-7f0aa98a04ac	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE	1
5557	141	MARICULTURE PRODUCTION	49da5018-59ec-4a60-9cb9-614ea6266ced	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > MARICULTURE PRODUCTION	1
5558	141	TOURISM	82fdb39c-4fe8-4e2b-9dcf-67ceb4c6d8b9	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > TOURISM	1
5559	142	CARBON CAPTURE AND STORAGE	e8c24822-7d2d-48c6-9dca-df3860e9bd63	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > CARBON CAPTURE AND STORAGE	1
5560	142	CARBON FOOTPRINT	0e530a5f-1e75-4602-9659-98ff5c3d7076	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > CARBON FOOTPRINT	1
5561	142	ENVIRONMENTAL ASSESSMENTS	079724fa-ff86-4195-aee0-51a4d6dd73bb	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > ENVIRONMENTAL ASSESSMENTS	1
5562	142	ENVIRONMENTAL REGULATIONS	57df059e-578a-4371-9484-7a34d63edfa5	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > ENVIRONMENTAL REGULATIONS	1
5563	142	FIRE MANAGEMENT	0ef4a2f0-8a29-4f5e-9396-b4f6a71c8bf6	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > FIRE MANAGEMENT	1
5564	142	GEOENGINEERING	262e3568-c57b-4e28-a142-ad5e7b51dfb7	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > GEOENGINEERING	1
5565	142	LAND MANAGEMENT	2be0af28-a6b8-4fce-82e4-1ad86788a4d5	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > LAND MANAGEMENT	1
5566	142	TREATY AGREEMENTS/RESULTS	4dad174d-9419-4634-84f0-7eeb1d517241	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > TREATY AGREEMENTS/RESULTS	1
5567	142	WATER MANAGEMENT	14555831-70ae-4650-8983-956d65595575	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > WATER MANAGEMENT	1
5568	143	ACID DEPOSITION	dbeff538-6857-4573-8d14-12009e0ee078	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > ACID DEPOSITION	1
5569	143	AGRICULTURAL EXPANSION	d076e628-320a-477b-aad9-07d87ca04993	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > AGRICULTURAL EXPANSION	1
5570	143	BIOCHEMICAL RELEASE	de89c42c-206a-4573-a2af-edffe5ddd6bf	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > BIOCHEMICAL RELEASE	1
5571	143	BIOMASS BURNING	9d7eed04-9c49-4024-8d0f-06474cc38bbc	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > BIOMASS BURNING	1
5572	143	CHEMICAL SPILLS	a5b074da-5e00-4fd9-9c40-cfec771263ee	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > CHEMICAL SPILLS	1
5573	143	CIVIL DISTURBANCE	09cf34f3-5e20-4dc1-9b76-97afd856ebe0	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > CIVIL DISTURBANCE	1
5574	143	CONSERVATION	40869a25-edea-4438-80f9-47c9e6910b9b	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > CONSERVATION	1
5575	143	CONTAMINANT LEVELS/SPILLS	912245ce-a81e-4d3b-b4fb-f71c8da63357	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > CONTAMINANT LEVELS/SPILLS	1
5576	143	ELECTRIC/MAGNETIC FIELD EXPOSURE	69d84440-b806-4093-a659-f052185e22bd	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > ELECTRIC/MAGNETIC FIELD EXPOSURE	1
5577	143	FOSSIL FUEL BURNING	edfbff1e-b24b-40b9-be54-e1823b4d7f49	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > FOSSIL FUEL BURNING	1
5578	143	GAS EXPLOSIONS/LEAKS	083d79ba-b7fa-4a07-9c36-73540666d5c4	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > GAS EXPLOSIONS/LEAKS	1
5579	143	GAS FLARING	6221fa7d-9407-4ffc-ab58-886038209254	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > GAS FLARING	1
5580	143	HEAVY METALS CONCENTRATION	0c4ffc6a-694d-4f33-bc18-06fefb68acdd	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > HEAVY METALS CONCENTRATION	1
5581	143	INDUSTRIAL EMISSIONS	07f7ea8e-cf94-4421-923a-539e12dbeb95	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > INDUSTRIAL EMISSIONS	1
5582	143	MINE DRAINAGE	207a34e0-48c0-439a-a001-dcf664b61686	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > MINE DRAINAGE	1
5583	143	NUCLEAR RADIATION EXPOSURE	48671d9e-a627-4034-baec-201bda5d166d	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > NUCLEAR RADIATION EXPOSURE	1
5584	143	OIL SPILLS	82c3689a-6bbf-496f-b118-b6ab46a9d2c7	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > OIL SPILLS	1
5585	143	PRESCRIBED BURNS/FIRES	c0fb4215-4f72-445f-af81-b3f44c44cd0e	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > PRESCRIBED BURNS/FIRES	1
5586	143	SEWAGE DISPOSAL	835c5ec2-50e3-4bef-b380-9f74b143dac6	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL IMPACTS > SEWAGE DISPOSAL	1
5587	144	DEFORESTATION	9a4715a7-1847-4fef-8116-494b36420fb7	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > DEFORESTATION	1
5588	144	DESERTIFICATION	dee57819-62c7-4f89-87e5-90a87a07820a	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > DESERTIFICATION	1
5589	144	ECOLOGICAL CORRIDORS	a66ec515-6a6e-487b-9004-2d19d6ffff04	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > ECOLOGICAL CORRIDORS	1
5590	144	EUTROPHICATION	32777aa3-a06a-4719-bbe5-7dcecb1a06f5	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > EUTROPHICATION	1
5591	144	IRRIGATION	59b3849e-6704-402f-9a3e-512db10c2f51	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > IRRIGATION	1
5592	144	RECLAMATION/REVEGETATION/RESTORATION	aa4a9df3-0fed-4512-b158-ed369463e33a	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > RECLAMATION/REVEGETATION/RESTORATION	1
5593	144	REFORESTATION/REVEGETATION	39a032bf-c3bc-481b-9698-8be114fe85cb	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > REFORESTATION/REVEGETATION	1
5594	144	URBANIZATION/URBAN SPRAWL	e759cacb-33f0-4564-b151-c7cfa5e85ed3	EARTH SCIENCE > HUMAN DIMENSIONS > HABITAT CONVERSION/FRAGMENTATION > URBANIZATION/URBAN SPRAWL	1
5595	145	ARCHAEOLOGICAL AREAS	bf703f22-9775-460d-86bd-149aaef1acde	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS > ARCHAEOLOGICAL AREAS	1
5596	145	COASTAL AREAS	b1f63bf1-a547-4189-9c7e-66a8d11facc4	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS > COASTAL AREAS	1
5597	145	RURAL AREAS	d83b4271-048c-4763-9d5c-b5ec1b1788f4	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS > RURAL AREAS	1
5598	145	TRIBAL LANDS	2b4df9a9-ac03-4bdc-bee4-346045a75e05	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS > TRIBAL LANDS	1
5599	145	URBAN AREAS	e4abd82b-b17a-4f16-be79-0093f2a09f7d	EARTH SCIENCE > HUMAN DIMENSIONS > HUMAN SETTLEMENTS > URBAN AREAS	1
5600	146	BUILDINGS	d7742082-5461-4610-9ced-e0ec3bb64697	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > BUILDINGS	1
5601	146	COMMUNICATIONS	db692676-a2f6-4fd9-91b6-92ae4f9c04fd	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > COMMUNICATIONS	1
5602	146	CULTURAL FEATURES	79b0b1d3-5279-4ce5-a387-6ecb4ee2a335	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > CULTURAL FEATURES	1
5603	146	ELECTRICITY	12433114-d15a-46cf-aba9-ce4b569119ce	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > ELECTRICITY	1
5604	146	GREEN INFRASTRUCTURE	eeba88d2-20bf-43b1-bccf-b125485405f4	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > GREEN INFRASTRUCTURE	1
5605	146	PIPELINES	ee49d315-1fe5-42ce-a5f8-232450dfa408	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > PIPELINES	1
5606	146	TRANSPORTATION	37a6c8e2-f2ac-48a4-a4fa-d80f700f68db	EARTH SCIENCE > HUMAN DIMENSIONS > INFRASTRUCTURE > TRANSPORTATION	1
5607	147	BIOLOGICAL HAZARDS	bb73336e-9113-426b-ac99-2b7c143b22ca	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > BIOLOGICAL HAZARDS	1
5608	147	DROUGHTS	115d340f-cb5e-4436-bfa4-04a740988bf7	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > DROUGHTS	1
5609	147	EARTHQUAKES	b3406120-9faa-4c00-874e-ce8878ae129f	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > EARTHQUAKES	1
5610	147	FAMINE	6bb02b3d-be70-47b0-93d7-eb0c926f5979	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > FAMINE	1
5611	147	FLOODS	fd03d204-4391-4e98-8142-8b8efa235231	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > FLOODS	1
5612	147	HEAT	bb9c9be6-78c7-4fbd-9a35-a218276393ec	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > HEAT	1
5613	147	LAND SUBSIDENCE	ba064d3f-0327-49d2-9984-332de1a97146	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > LAND SUBSIDENCE	1
5614	147	LANDSLIDES	f81d3752-d97c-4caf-9a79-5709ee693158	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > LANDSLIDES	1
5615	147	SEVERE STORMS	ad28623e-bb9b-433c-8fc1-2ab06dda58c4	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > SEVERE STORMS	1
5616	147	TORNADOES	ff44a7b0-64b6-418a-9d74-1cbc3a4ae951	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TORNADOES	1
5617	147	TROPICAL CYCLONES	00fc45e0-400d-4024-a82a-4d6544735f64	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES	1
5618	147	TSUNAMIS	768f266e-0807-49c6-a69e-c518de310331	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TSUNAMIS	1
5619	147	VOLCANIC ERUPTIONS	06c1281f-e306-4511-bdab-ed6c0694f0f9	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > VOLCANIC ERUPTIONS	1
5620	147	WILDFIRES	868b87a1-d8c2-49b3-8bbd-9cbbed115271	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > WILDFIRES	1
5621	148	MORTALITY	3fd888c4-2fd2-4ce1-8753-3158e2826ef7	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > MORTALITY	1
5622	148	NATALITY	9d6eda76-cf5d-4170-92ce-9ac9197832bf	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > NATALITY	1
5623	148	POPULATION DENSITY	d2a5c7ec-ccf2-4ab7-8863-9063be91c022	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > POPULATION DENSITY	1
5624	148	POPULATION DISTRIBUTION	ae9f3a07-f23e-4116-b172-677435102b2f	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > POPULATION DISTRIBUTION	1
5625	148	POPULATION ESTIMATES	d7ad5cff-75df-4bb6-92f0-b5d56da2a588	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > POPULATION ESTIMATES	1
5626	148	POPULATION SIZE	dd0b8bc9-90b3-4e7d-a021-e91dc676d622	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > POPULATION SIZE	1
5834	170	HYPOXIA	b846063c-e218-4fc6-9866-0cdca24e9023	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > HYPOXIA	1
5627	148	VULNERABLE POPULATIONS	35b7c7cd-49c8-476c-83f2-f2e1f4097307	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > VULNERABLE POPULATIONS	1
5628	149	DISEASES/EPIDEMICS	7d59f070-ccac-4a90-815b-edfca521779b	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS	1
5629	149	ENVIRONMENTAL HEALTH FACTORS	5a47842e-785d-4cc4-b1c1-2147a9252c19	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > ENVIRONMENTAL HEALTH FACTORS	1
5630	149	FOOD SECURITY	85a73755-cb84-40cb-a23e-2ed3811138f8	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > FOOD SECURITY	1
5631	149	MALNUTRITION	1d1f1722-27ea-4021-922f-68b90c09bfa1	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > MALNUTRITION	1
5632	149	MENTAL HEALTH IMPACTS	3ad043a9-2ec8-401d-a727-5589a303ea4a	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > MENTAL HEALTH IMPACTS	1
5633	149	MORBIDITY	8a49484a-a9c8-411b-b911-7646f5323a7b	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > MORBIDITY	1
5634	149	RADIATION EXPOSURE	74851074-27ab-425b-9521-8d139b907b0d	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > RADIATION EXPOSURE	1
5635	149	WATER TREATMENT DISRUPTION	91df78a1-2e38-41d5-b88e-e235450c89fc	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > WATER TREATMENT DISRUPTION	1
5636	150	CONSERVATION	aef9855c-70e1-4e22-aa25-8ccd23176d3b	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > CONSERVATION	1
5637	150	CONSUMER BEHAVIOR	d11d5e6d-fafb-4012-818c-8bfb984128f1	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > CONSUMER BEHAVIOR	1
5638	150	DISASTER RESPONSE	507860e1-7494-438a-8537-b21da89efddf	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > DISASTER RESPONSE	1
5639	150	HAZARD MITIGATION/PLANNING	843a6584-e3f2-4a75-a003-cc430fd8c22c	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > HAZARD MITIGATION/PLANNING	1
5640	150	PRESERVATION	859155e1-d2d3-41a3-8d44-91afa87d68b4	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > PRESERVATION	1
5641	150	RECREATIONAL ACTIVITIES/AREAS	9ee8acad-458e-45c1-a1d5-9b1649c82ea7	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > RECREATIONAL ACTIVITIES/AREAS	1
5642	150	RECYCLING	b2f12641-19c8-4b26-9496-e79da5efcb85	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > RECYCLING	1
5643	150	VULNERABILITY LEVELS/INDEX	33f20afe-5ce2-43e9-9676-c5f664fbc324	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIAL BEHAVIOR > VULNERABILITY LEVELS/INDEX	1
5644	151	HOUSEHOLD INCOME	c88a747b-2302-49c9-b747-f2faa21e2b6b	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIOECONOMICS > HOUSEHOLD INCOME	1
5645	151	INDUSTRIALIZATION	92d8968b-617e-433d-ab9b-e269497c3f43	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIOECONOMICS > INDUSTRIALIZATION	1
5646	151	POVERTY LEVELS	b37021a3-4d7f-4b94-b614-807d6981d2ad	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIOECONOMICS > POVERTY LEVELS	1
5647	151	PURCHASING POWER	2bf46486-3004-447e-b2c6-82c4aa13fc11	EARTH SCIENCE > HUMAN DIMENSIONS > SOCIOECONOMICS > PURCHASING POWER	1
5648	152	ENVIRONMENTAL SUSTAINABILITY	73266dd6-217a-432f-9237-176d3e94b39b	EARTH SCIENCE > HUMAN DIMENSIONS > SUSTAINABILITY > ENVIRONMENTAL SUSTAINABILITY	1
5649	152	SUSTAINABLE DEVELOPMENT	8d11c81c-ff5b-4cc0-9be2-8e73dddcb51b	EARTH SCIENCE > HUMAN DIMENSIONS > SUSTAINABILITY > SUSTAINABLE DEVELOPMENT	1
5650	153	DEGRADATION	2f2f5764-d4e6-4bbb-bd6d-dda373018237	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > DEGRADATION	1
5651	153	ENTRAINMENT	f6a5cc87-a333-4e99-88d4-bf7b5b1cf484	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > ENTRAINMENT	1
5652	153	EROSION	1e2b1b67-a401-4fb6-9ee9-b022c1c023dc	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > EROSION	1
5653	153	LANDSLIDES	ea4aefeb-64cd-4408-83d8-8e0a672739b9	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > LANDSLIDES	1
5654	153	SEDIMENT CHEMISTRY	ca2ffcd6-39e6-4eab-abc2-07eb4a197e3d	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SEDIMENT CHEMISTRY	1
5655	153	SEDIMENT COMPOSITION	807aff1a-6fe0-474a-a025-a0d0d8b17dbd	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SEDIMENT COMPOSITION	1
5656	153	SEDIMENT TRANSPORT	e4ad5a76-7540-4433-ad82-9fe89259538b	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SEDIMENT TRANSPORT	1
5657	153	SEDIMENTATION	b41498cd-6b2b-47e3-afe7-0f05b4c0807d	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SEDIMENTATION	1
5658	153	SEDIMENTS	26558c08-beca-4ef0-9ea3-b000504ece60	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SEDIMENTS	1
5659	153	STRATIGRAPHIC SEQUENCE	42b5ae5b-90d5-44f0-b331-6c22cdd45c3f	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
5660	153	SUSPENDED SOLIDS	69ff701a-674e-4b63-bb93-6ebe6cd95281	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > SUSPENDED SOLIDS	1
5661	153	WEATHERING	b07017e8-d714-45a6-b1fe-8c00230ec209	EARTH SCIENCE > LAND SURFACE > EROSION/SEDIMENTATION > WEATHERING	1
5662	154	ACTIVE LAYER	10270ee0-8d85-4c75-9fa2-49e7a9755cb3	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > ACTIVE LAYER	1
5663	154	CRYOSOLS	1469f30b-6eb4-4186-b1ef-7dd25c34c592	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > CRYOSOLS	1
5664	154	GROUND ICE	5b4dde5a-733e-4e55-97c9-2108b337cfeb	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > GROUND ICE	1
5665	154	PERIGLACIAL PROCESSES	5181e50a-b1d2-41b1-bde3-fd9b4da9b1bf	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > PERIGLACIAL PROCESSES	1
5666	154	PERMAFROST	b6723314-3db7-4bdd-85ee-0b8507e6ae1b	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > PERMAFROST	1
5667	154	ROCK GLACIERS	ee2af62b-9f76-440c-aa9b-77940468b8f4	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > ROCK GLACIERS	1
5668	154	SEASONALLY FROZEN GROUND	6fdd8021-3f6f-4f54-829c-26f744597309	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > SEASONALLY FROZEN GROUND	1
5669	154	SOIL TEMPERATURE	240ff021-6a9c-4603-983d-f135ee7e49ab	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > SOIL TEMPERATURE	1
5670	154	TALIK	c39710ae-423f-44c8-b969-9af8a1f912cf	EARTH SCIENCE > LAND SURFACE > FROZEN GROUND > TALIK	1
5671	155	AEOLIAN LANDFORMS	ed75fb8f-cb96-448e-ada5-dc48fbd0ebb1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS	1
5672	155	AEOLIAN PROCESSES	3ab3aa92-9cca-4660-a0ed-281fff07eede	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES	1
5673	155	COASTAL LANDFORMS	0cff6e4b-e42a-4565-89ff-350adf41ed69	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS	1
5674	155	COASTAL PROCESSES	e26803a0-82ea-40c4-a41a-9e222c9bd09a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES	1
5675	155	FLUVIAL LANDFORMS	bdc0bd86-a3a3-48fa-b1fb-4ca5d13d4dde	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS	1
5676	155	FLUVIAL PROCESSES	4b982bef-56fe-41e9-a131-af575a8fec6a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES	1
5677	155	GLACIAL LANDFORMS	b895f4b5-5273-49ef-883f-b67d9f199505	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS	1
5678	155	GLACIAL PROCESSES	b409a30b-0e3f-4592-bec9-7d371797b4a9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES	1
5679	155	KARST LANDFORMS	590aa85e-bbce-40b2-8ffb-53d80a61c51a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS	1
5680	155	KARST PROCESSES	9cd875b0-210b-458f-b208-1690f50820d0	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES	1
5681	155	TECTONIC LANDFORMS	9673dc0b-89c0-4f0c-b378-f1c8cb267c8f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS	1
5682	155	TECTONIC PROCESSES	99b4792a-9ea3-4756-a4dc-b1b30c946b54	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES	1
5683	156	LAND PRODUCTIVITY	2e69c08b-ee0f-426c-a8d2-dc50876f76c2	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND PRODUCTIVITY	1
5684	156	LAND RESOURCES	c77819e9-f62f-48dc-b924-e7a73b4dcda9	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND RESOURCES	1
5685	156	LAND USE CLASSES	fe2f8240-4d8e-4b1f-b869-29fee59692f7	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND USE CLASSES	1
5686	156	LAND USE/LAND COVER CLASSIFICATION	75c312bc-79f9-4d74-a7c0-3c67c019196c	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND USE/LAND COVER CLASSIFICATION	1
5687	157	LANDSCAPE ECOLOGY	e77c0096-05a7-47ff-8629-55d12c46bb6b	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > LANDSCAPE ECOLOGY	1
5688	157	LANDSCAPE MANAGEMENT	36a4ac5a-1082-4922-9bca-934c06e54cda	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > LANDSCAPE MANAGEMENT	1
5689	157	LANDSCAPE PATTERNS	3b6fe940-7383-4bae-b436-fc487723bbcf	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > LANDSCAPE PATTERNS	1
5690	157	LANDSCAPE PROCESSES	6c44a08d-0a08-47f5-b819-7e561445e613	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > LANDSCAPE PROCESSES	1
5691	157	RECLAMATION/REVEGETATION/RESTORATION	d57dff3d-5f2f-425c-80bb-2a6fcb42d3fa	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > RECLAMATION/REVEGETATION/RESTORATION	1
5692	157	REFORESTATION	dcb100c9-5b43-422a-a429-25cae9dbb170	EARTH SCIENCE > LAND SURFACE > LANDSCAPE > REFORESTATION	1
5693	158	CALCIUM	9409ee0f-2b72-4472-9d61-f8072981a6cb	EARTH SCIENCE > LAND SURFACE > SOILS > CALCIUM	1
5694	158	CARBON	a7ae5843-479c-4055-b8fc-ba651e485750	EARTH SCIENCE > LAND SURFACE > SOILS > CARBON	1
5695	158	CATION EXCHANGE CAPACITY	9bad3c7b-daf6-428a-89bd-ce62b074dfcf	EARTH SCIENCE > LAND SURFACE > SOILS > CATION EXCHANGE CAPACITY	1
5696	158	DENITRIFICATION RATE	0d0de6a7-c340-4e6b-b01d-ccbb6e7fa913	EARTH SCIENCE > LAND SURFACE > SOILS > DENITRIFICATION RATE	1
5697	158	ELECTRICAL CONDUCTIVITY	781bf38b-2797-4415-8d5a-67e9f3a2f5fe	EARTH SCIENCE > LAND SURFACE > SOILS > ELECTRICAL CONDUCTIVITY	1
5698	158	HEAVY METALS	49ee4fcc-a0ad-4638-aec9-90b4946d8922	EARTH SCIENCE > LAND SURFACE > SOILS > HEAVY METALS	1
5699	158	HYDRAULIC CONDUCTIVITY	e2a88ac8-7bf3-408c-b2b4-b3217f9e4917	EARTH SCIENCE > LAND SURFACE > SOILS > HYDRAULIC CONDUCTIVITY	1
5700	158	MACROFAUNA	5c4b5f03-8e57-49f0-bb03-f8efafb837d3	EARTH SCIENCE > LAND SURFACE > SOILS > MACROFAUNA	1
5701	158	MAGNESIUM	7b86bc20-ba2b-4cd0-8aa0-ed47663d9222	EARTH SCIENCE > LAND SURFACE > SOILS > MAGNESIUM	1
5702	158	MICROFAUNA	e9555194-efd1-4427-b8e3-8fe6c49b8636	EARTH SCIENCE > LAND SURFACE > SOILS > MICROFAUNA	1
5703	158	MICROFLORA	ed1b3fa6-173d-476c-9b35-c57335c0a473	EARTH SCIENCE > LAND SURFACE > SOILS > MICROFLORA	1
5704	158	MICRONUTRIENTS/TRACE ELEMENTS	ac061db6-21c7-46fc-b5a8-9f61c795fdd6	EARTH SCIENCE > LAND SURFACE > SOILS > MICRONUTRIENTS/TRACE ELEMENTS	1
5705	158	NITROGEN	e1179e7f-59e5-465a-9879-6bda6985744e	EARTH SCIENCE > LAND SURFACE > SOILS > NITROGEN	1
5706	158	ORGANIC MATTER	215f69b9-259a-4b82-9f8f-f96d4f5aaad2	EARTH SCIENCE > LAND SURFACE > SOILS > ORGANIC MATTER	1
5707	158	PERMAFROST	08240c92-00b5-4f25-bf2e-8030531a78d2	EARTH SCIENCE > LAND SURFACE > SOILS > PERMAFROST	1
5708	158	PHOSPHORUS	9169ace5-0f04-4fc9-b38d-b89a786b9fe1	EARTH SCIENCE > LAND SURFACE > SOILS > PHOSPHORUS	1
5709	158	POTASSIUM	8af17fd3-7c42-4698-9d60-e154ece5aebe	EARTH SCIENCE > LAND SURFACE > SOILS > POTASSIUM	1
5710	158	RECLAMATION/REVEGETATION/RESTORATION	c22818ce-07aa-4f77-8fe2-be1925743bac	EARTH SCIENCE > LAND SURFACE > SOILS > RECLAMATION/REVEGETATION/RESTORATION	1
5711	158	SOIL ABSORPTION	e497c2e3-cd21-4af9-9a5d-91da4e201631	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL ABSORPTION	1
5712	158	SOIL BULK DENSITY	2c821621-f035-4c57-8dee-5f24968f959a	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL BULK DENSITY	1
5713	158	SOIL CHEMISTRY	e273b634-62f5-4601-8b92-6550f6efeab8	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL CHEMISTRY	1
5714	158	SOIL CLASSIFICATION	14e51b6e-9d91-4af5-bb93-22842359d492	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL CLASSIFICATION	1
5715	158	SOIL COLOR	013b44e9-df5c-4ef8-a99f-7351d16bfd14	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL COLOR	1
5716	158	SOIL COMPACTION	c9f8c1e9-dca8-4c2e-9537-65903d19cfe5	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL COMPACTION	1
5717	158	SOIL CONSISTENCE	6ce3eeff-d222-4356-8cd2-50fbcbcbb295	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL CONSISTENCE	1
5718	158	SOIL DEPTH	60e783c1-4b33-4ab3-860b-8bd4ed00dc9f	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL DEPTH	1
5719	158	SOIL EROSION	6eef914d-ff9f-44b0-a3a6-3dcf911023d4	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL EROSION	1
5720	158	SOIL FERTILITY	cdb10789-ef01-46bd-8047-86e550df0df4	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL FERTILITY	1
5721	158	SOIL GAS/AIR	76c23076-d9d5-4414-a69f-a830cecdd9ce	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL GAS/AIR	1
5722	158	SOIL HEAT BUDGET	c6847d01-cbf9-491b-be59-c283d9072d95	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL HEAT BUDGET	1
5723	158	SOIL HORIZONS/PROFILE	7a16aa40-c74b-4a69-a230-1edd1b453332	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL HORIZONS/PROFILE	1
5724	158	SOIL IMPEDANCE	bcc72093-b2d4-47e8-9213-7f48172e0e95	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL IMPEDANCE	1
5725	158	SOIL INFILTRATION	2283a2fe-19ec-4b1d-a553-20ec9713a658	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL INFILTRATION	1
5726	158	SOIL MECHANICS	e9d5ae5a-0718-44f2-9694-b791b646a825	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL MECHANICS	1
5727	158	SOIL MOISTURE/WATER CONTENT	bbe2ea34-8842-4a9f-9b0b-95dd3c71857f	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL MOISTURE/WATER CONTENT	1
5729	158	SOIL PLASTICITY	2da4e52a-b43b-4ff0-9e4d-c98438a38c6d	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL PLASTICITY	1
5730	158	SOIL POROSITY	20f932b9-cc40-4462-879f-1c8d8c765152	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL POROSITY	1
5731	158	SOIL PRODUCTIVITY	1e7afff2-cd50-4d26-968b-bffd2d738edd	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL PRODUCTIVITY	1
5732	158	SOIL RESPIRATION	e699830a-0abf-45b2-8026-ac80e0269ea7	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL RESPIRATION	1
5733	158	SOIL ROOTING DEPTH	1b475201-a032-4a66-a3aa-a35605affaee	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL ROOTING DEPTH	1
5734	158	SOIL SALINITY/SOIL SODICITY	9d7b0259-2d88-4e78-b2c2-131a02d05c15	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL SALINITY/SOIL SODICITY	1
5735	158	SOIL STRUCTURE	aa25235a-596f-4504-89e1-4c625275700d	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL STRUCTURE	1
5736	158	SOIL TEMPERATURE	0546b91a-294d-45d9-8b45-76aaad0cc024	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL TEMPERATURE	1
5737	158	SOIL TEXTURE	fb05c0c0-7fcd-470c-ba2b-755f04f5d811	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL TEXTURE	1
5738	158	SOIL WATER HOLDING CAPACITY	7c00e468-6a43-49ef-891e-b0ce29e2ff36	EARTH SCIENCE > LAND SURFACE > SOILS > SOIL WATER HOLDING CAPACITY	1
5739	158	SULFUR	742e6889-1ebf-4441-b803-4892c7176822	EARTH SCIENCE > LAND SURFACE > SOILS > SULFUR	1
5740	158	THERMAL CONDUCTIVITY	c67c1e1c-19f1-49de-8b2b-d5ce6f596323	EARTH SCIENCE > LAND SURFACE > SOILS > THERMAL CONDUCTIVITY	1
5741	159	ALBEDO	136b1de3-4b2e-49e6-80cd-cf2e9bac2c48	EARTH SCIENCE > LAND SURFACE > SURFACE RADIATIVE PROPERTIES > ALBEDO	1
5742	159	ANISOTROPY	00c1d7b9-61d8-40ad-8c33-f27006832866	EARTH SCIENCE > LAND SURFACE > SURFACE RADIATIVE PROPERTIES > ANISOTROPY	1
5743	159	EMISSIVITY	4ee9d0c5-2e0c-486c-b89b-7b002d18c5f7	EARTH SCIENCE > LAND SURFACE > SURFACE RADIATIVE PROPERTIES > EMISSIVITY	1
5744	159	REFLECTANCE	f043c0a8-9cee-4c51-bf64-a4aaa34ab75d	EARTH SCIENCE > LAND SURFACE > SURFACE RADIATIVE PROPERTIES > REFLECTANCE	1
5745	160	LAND HEAT CAPACITY	8931329c-3f6d-4ba6-913c-27afa8d104c1	EARTH SCIENCE > LAND SURFACE > SURFACE THERMAL PROPERTIES > LAND HEAT CAPACITY	1
5746	160	LAND SURFACE TEMPERATURE	d559b900-eca6-42a4-9311-0297b2ef98ab	EARTH SCIENCE > LAND SURFACE > SURFACE THERMAL PROPERTIES > LAND SURFACE TEMPERATURE	1
5747	160	SKIN TEMPERATURE	40d6a3e7-89dd-4399-8fa5-bbc7a0917b4e	EARTH SCIENCE > LAND SURFACE > SURFACE THERMAL PROPERTIES > SKIN TEMPERATURE	1
5748	161	SURFACE ROUGHNESS	21474df3-f9a6-48ca-be15-bdb3611fe062	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > SURFACE ROUGHNESS	1
5749	161	TERRAIN ELEVATION	74ed1690-968e-444c-8a31-7b8344a2aad3	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TERRAIN ELEVATION	1
5750	161	TOPOGRAPHIC EFFECTS	05bef198-cfff-48be-b0cb-14e296d38dbc	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TOPOGRAPHIC EFFECTS	1
5751	162	AQUACULTURE	f6c057c9-c789-4cd5-ba22-e9b08aae152b	EARTH SCIENCE > OCEANS > AQUATIC SCIENCES > AQUACULTURE	1
5752	162	FISHERIES	fa57b0a0-9723-4195-bdd1-4f26aefa0e07	EARTH SCIENCE > OCEANS > AQUATIC SCIENCES > FISHERIES	1
5753	163	ABYSSAL HILLS/PLAINS	0b011562-ee55-4ba0-a026-4faa7493ca5b	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > ABYSSAL HILLS/PLAINS	1
5754	163	BATHYMETRY	80d79c7e-6c64-4ada-bfcc-4093969758a5	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > BATHYMETRY	1
5755	163	CONTINENTAL MARGINS	a91a00f7-05ed-4633-9fac-1772a48b6342	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > CONTINENTAL MARGINS	1
5756	163	FRACTURE ZONES	58c12630-a889-44c1-a951-56bbbe9758c9	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > FRACTURE ZONES	1
5757	163	OCEAN PLATEAUS/RIDGES	73e02157-9df9-415f-93fc-cb457989ddb1	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > OCEAN PLATEAUS/RIDGES	1
5758	163	SEAFLOOR TOPOGRAPHY	b6b51058-1111-4498-a9ac-e1515270fb27	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > SEAFLOOR TOPOGRAPHY	1
5759	163	SEAMOUNTS	83520258-413c-4842-93c0-58a23dc58638	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > SEAMOUNTS	1
5760	163	SUBMARINE CANYONS	18ce5577-26e9-4b76-860b-1ba31cafa9d0	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > SUBMARINE CANYONS	1
5761	163	TRENCHES	36040c6a-5e3a-49fe-b519-162fb77a0fd4	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > TRENCHES	1
5762	163	WATER DEPTH	ca477721-473b-40d7-a72b-4ffa963e48fb	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH	1
5763	164	BARRIER ISLANDS	7e28f2e0-a641-4085-be07-366ed6e701f4	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > BARRIER ISLANDS	1
5764	164	BEACHES	4ba798ce-ad0b-4809-94fa-ec1b8e294252	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > BEACHES	1
5765	164	COASTAL ELEVATION	1fbf5df2-ab7c-43fc-9bb2-8eb3f8891f7b	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > COASTAL ELEVATION	1
5766	164	CORAL REEFS	ad497e7a-48fa-45e1-90a5-b052508bdb30	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > CORAL REEFS	1
5767	164	DELTAS	f9f0f92b-7901-4dda-8d64-be4e845ce29b	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > DELTAS	1
5768	164	DUNES	6f7b2753-aed1-4783-a7cc-781d00d13a0f	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > DUNES	1
5769	164	EROSION	cd7a7748-7231-4a73-b85c-b5696066230a	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > EROSION	1
5770	164	ESTUARIES	a7dcdedf-bcc5-4032-b70f-7fadf74d6144	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > ESTUARIES	1
5771	164	FJORDS	a90899c8-fe50-48e0-b92c-bb64f6ae681c	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > FJORDS	1
5772	164	INLETS	f43cd776-c568-4d09-997c-0a8ad1022e06	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > INLETS	1
5773	164	INTERTIDAL ZONE	82b62e59-6ea1-48e1-a402-bd386c5046eb	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > INTERTIDAL ZONE	1
5774	164	LAGOONS	c733c179-c12a-47e9-8e9a-817a5212446f	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > LAGOONS	1
5775	164	LOCAL SUBSIDENCE TRENDS	5a090f0c-7466-47fd-b679-5dee947ab05c	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > LOCAL SUBSIDENCE TRENDS	1
5776	164	LONGSHORE CURRENTS	ccf07d90-b3a3-43d3-9249-a494bb48d1b6	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > LONGSHORE CURRENTS	1
5777	164	MANGROVES	04c4a85f-91ce-4d64-9e19-b3e0897ff187	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > MANGROVES	1
5778	164	MARSHES	30056645-a442-4ef6-ac76-c5bc27086d83	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > MARSHES	1
5779	164	ROCKY COASTS	488f4df2-712e-4fac-98d1-46ab134b84ee	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > ROCKY COASTS	1
5780	164	SALTWATER INTRUSION	dffe5a35-09af-4413-bdd3-a5aedfeb49cc	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SALTWATER INTRUSION	1
5781	164	SEA LEVEL RISE	0afaaa5e-f88c-4c1f-95c1-1faa0148885a	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SEA LEVEL RISE	1
5782	164	SEA SURFACE HEIGHT	1ed24fe1-d0d5-46d1-8d22-8ac25d289c75	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SEA SURFACE HEIGHT	1
5783	164	SEDIMENT TRANSPORT	c5c34f0a-552e-45a6-91c1-9edb3a8deef9	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SEDIMENT TRANSPORT	1
5784	164	SEDIMENTATION	9457740a-897b-4adc-96fb-f3e3aafa34ea	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SEDIMENTATION	1
5785	164	SHOALS	4c2d2255-680d-47d6-adb2-179093593f8a	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SHOALS	1
5786	164	SHORELINE DISPLACEMENT	1a740c3e-7032-4f72-93e8-d0ba343d82e0	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SHORELINE DISPLACEMENT	1
5787	164	SHORELINES	1d3b4eb7-9931-44bf-8457-26847051b7a8	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > SHORELINES	1
5788	164	STORM SURGE	9edd23d0-68a9-4bae-8887-705058f48ba7	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > STORM SURGE	1
5789	164	TIDAL HEIGHT	9ab67e8f-066e-47b8-838d-8cd5e7460119	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > TIDAL HEIGHT	1
5790	165	MARINE OBSTRUCTIONS	56e4dd42-e393-4aa2-b4d9-9e96d85c9768	EARTH SCIENCE > OCEANS > MARINE ENVIRONMENT MONITORING > MARINE OBSTRUCTIONS	1
5791	166	MAGNETIC ANOMALIES	e31f905d-bd2a-4fe9-89d8-909e1d2b9b1a	EARTH SCIENCE > OCEANS > MARINE GEOPHYSICS > MAGNETIC ANOMALIES	1
5792	166	MARINE GRAVITY FIELD	ad09b215-e837-4d9f-acbc-2b45e5b81825	EARTH SCIENCE > OCEANS > MARINE GEOPHYSICS > MARINE GRAVITY FIELD	1
5793	166	MARINE MAGNETICS	7863ce31-0e06-42a5-bcf8-25981c44dec8	EARTH SCIENCE > OCEANS > MARINE GEOPHYSICS > MARINE MAGNETICS	1
5794	166	PLATE TECTONICS	78a4dbe2-2d6b-4562-988c-022c3a83f4c1	EARTH SCIENCE > OCEANS > MARINE GEOPHYSICS > PLATE TECTONICS	1
5795	167	BIOGENIC SEDIMENTS	ff0108e2-8415-423c-85ed-07792dbef534	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > BIOGENIC SEDIMENTS	1
5796	167	BIOTURBATION	14c8935f-8a46-4111-8f2e-bec8bbae5d13	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > BIOTURBATION	1
5797	167	DIAGENESIS	4bfed15d-b8b4-4fb1-940b-ef342c4c2225	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > DIAGENESIS	1
5798	167	GEOTECHNICAL PROPERTIES	d4f4b5d3-27b2-4b7d-bb69-733b67ac687a	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > GEOTECHNICAL PROPERTIES	1
5799	167	HYDROGENOUS SEDIMENTS	3d352f0f-f69f-44c4-b345-aa9230fbd6ca	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > HYDROGENOUS SEDIMENTS	1
5800	167	PARTICLE FLUX	676327f4-8354-4033-8081-9cab6651ac98	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > PARTICLE FLUX	1
5801	167	SEDIMENT CHEMISTRY	f8411549-a72d-44cd-9b7b-6953ec22f8da	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENT CHEMISTRY	1
5802	167	SEDIMENT COMPOSITION	17008d04-394d-4de8-8834-dd0a3cd88093	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENT COMPOSITION	1
5803	167	SEDIMENT TRANSPORT	bd55adac-4182-4441-91e2-163aa77e1320	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENT TRANSPORT	1
5804	167	SEDIMENTARY STRUCTURES	282ea985-efd0-4113-860d-b8221f6cc6f2	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENTARY STRUCTURES	1
5805	167	SEDIMENTARY TEXTURES	cddc37fd-8540-4c78-b567-add74e6b789b	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENTARY TEXTURES	1
5806	167	SEDIMENTATION	a4eb3bc4-48a5-4ed2-a74b-ca87a58e90f5	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SEDIMENTATION	1
5807	167	STRATIGRAPHIC SEQUENCE	41b7293f-7f20-40ab-8bf7-b211c68146b9	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > STRATIGRAPHIC SEQUENCE	1
5808	167	SUSPENDED SOLIDS	bcf6975f-2a21-4a6c-9286-fb8f85d00901	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > SUSPENDED SOLIDS	1
5809	167	TERRIGENOUS SEDIMENTS	31cf96eb-7fcd-490d-9e10-7f17dc12e1e3	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > TERRIGENOUS SEDIMENTS	1
5810	167	TURBIDITY	68e2c729-f729-4936-af2e-0ecf7ee7d231	EARTH SCIENCE > OCEANS > MARINE SEDIMENTS > TURBIDITY	1
5811	168	BENTHIC HEAT FLOW	bf3d6238-d0d6-4e73-82e6-5e38bc9291bb	EARTH SCIENCE > OCEANS > MARINE VOLCANISM > BENTHIC HEAT FLOW	1
5812	168	HYDROTHERMAL VENTS	b677862b-7921-458f-a6db-0eb46469df33	EARTH SCIENCE > OCEANS > MARINE VOLCANISM > HYDROTHERMAL VENTS	1
5813	168	ISLAND ARCS	9bb0de49-1812-400c-a73b-d2686dd9066a	EARTH SCIENCE > OCEANS > MARINE VOLCANISM > ISLAND ARCS	1
5814	168	MID-OCEAN RIDGES	f345294c-36e6-4c76-b484-2204cc0bc3a2	EARTH SCIENCE > OCEANS > MARINE VOLCANISM > MID-OCEAN RIDGES	1
5815	168	RIFT VALLEYS	f32afbca-dac6-41b1-a198-791c1fb57951	EARTH SCIENCE > OCEANS > MARINE VOLCANISM > RIFT VALLEYS	1
5816	169	ACOUSTIC ATTENUATION/TRANSMISSION	025c1e31-1a97-4a30-a887-0b9a5127fd4d	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC ATTENUATION/TRANSMISSION	1
5817	169	ACOUSTIC FREQUENCY	7bb3c4cd-cbb4-4c82-997b-d11ecc1cdb9f	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC FREQUENCY	1
5818	169	ACOUSTIC REFLECTIVITY	6a583047-6023-4b6a-ab25-b72529721a8c	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC REFLECTIVITY	1
5819	169	ACOUSTIC SCATTERING	b4a924bb-0d42-4169-bad7-3856f69f0c4a	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC SCATTERING	1
5820	169	ACOUSTIC TOMOGRAPHY	1295cf9a-c345-40eb-9b79-82bddc6acf50	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC TOMOGRAPHY	1
5821	169	ACOUSTIC VELOCITY	e4aae1a4-b4d5-4b13-9cc0-c0df6234ce3b	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > ACOUSTIC VELOCITY	1
5822	169	AMBIENT NOISE	a74abbc1-dd75-4f22-bbec-7d45091a4593	EARTH SCIENCE > OCEANS > OCEAN ACOUSTICS > AMBIENT NOISE	1
5823	170	ALKALINITY	4eab7956-e59e-4615-8d5c-39a16faa1f27	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > ALKALINITY	1
5824	170	AMMONIA	64d17528-29b4-4e2e-843a-7f7035bb5717	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > AMMONIA	1
5825	170	BIOGEOCHEMICAL CYCLES	f1e6caa5-2c97-407d-a0db-7bf01794d8e3	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > BIOGEOCHEMICAL CYCLES	1
5826	170	BIOMEDICAL CHEMICALS	97636cf7-189f-4953-9807-64fbcc60f72c	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > BIOMEDICAL CHEMICALS	1
5827	170	CARBON DIOXIDE	26afa886-4866-4536-be3a-6f9db9aacd97	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > CARBON DIOXIDE	1
5828	170	CARBONATE	68f7ba1b-a2f9-41b6-9bc1-fd187942fbed	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > CARBONATE	1
5829	170	CARBON	5c52009f-2c44-4db1-b62b-135c6181bad2	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > CARBON	1
5830	170	CHLOROPHYLL	7989eae1-8ea3-4039-af0c-9130de145449	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > CHLOROPHYLL	1
5831	170	DISSOLVED GASES	38219b66-2acd-4f77-a0fc-8241172c9001	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > DISSOLVED GASES	1
5832	170	DISSOLVED SOLIDS	a3c25ed5-d3e4-4b86-bd9a-6f78d5d2bc07	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > DISSOLVED SOLIDS	1
5833	170	HYDROCARBONS	6d8eb011-ffb5-4e18-ac59-2d8f84353734	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > HYDROCARBONS	1
5835	170	INORGANIC CARBON	d9b4f30d-bddd-4888-b66b-07d2dc09708b	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > INORGANIC CARBON	1
5836	170	INORGANIC MATTER	b9cfc6af-a424-42b9-8e89-6b332262e841	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > INORGANIC MATTER	1
5837	170	MARINE GEOCHEMISTRY	1dfb36a3-f985-4514-a1d0-cc73ca572922	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > MARINE GEOCHEMISTRY	1
5838	170	NITRATE	4fde380a-38c5-4d46-bc80-4f2515a43983	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITRATE	1
5839	170	NITRIC ACID	61740c18-f010-4384-8516-1eb33d75352e	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITRIC ACID	1
5840	170	NITRITE	941410da-0b7f-4ec6-a718-212194ced13f	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITRITE	1
5841	170	NITROGEN DIOXIDE	54054bc3-5faa-4b0d-b5dd-cf04595369b5	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITROGEN DIOXIDE	1
5842	170	NITROGEN	db5357c9-cc9d-4693-86fe-6bb88555d434	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITROGEN	1
5843	170	NITROUS OXIDE	d1c2bba5-799d-412b-80e0-fa04058416e3	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NITROUS OXIDE	1
5844	170	NUTRIENTS	8dd7c9f0-51d0-4037-b1d0-a2517c1770ad	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > NUTRIENTS	1
5845	170	OCEAN TRACERS	080db90f-79ff-4900-941d-9c02fe2df862	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > OCEAN TRACERS	1
5846	170	ORGANIC CARBON	d3055f47-258e-4556-a885-54cd1fff4680	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > ORGANIC CARBON	1
5847	170	ORGANIC MATTER	b2bdeb71-81b5-43e6-a8b1-b09c215c8d1a	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > ORGANIC MATTER	1
5848	170	OXYGEN	90aa8838-79bd-4b28-b518-8217e863c385	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > OXYGEN	1
5849	170	PHOSPHATE	0b513d8c-bfd3-44ee-976e-42757b8375a2	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > PHOSPHATE	1
5850	170	PH	4433600b-f323-458a-b295-352f939aab6b	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > PH	1
5851	170	PIGMENTS	ed925b43-db83-4cbb-8347-3dc0081bb8f4	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > PIGMENTS	1
5852	170	RADIOCARBON	6641ff15-36c8-4dbc-bf9c-176a08688173	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > RADIOCARBON	1
5853	170	RADIONUCLIDES	e9ed684e-5252-4091-a794-aaf6e5f249ed	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > RADIONUCLIDES	1
5854	170	SILICATE	c91c8879-1b29-48e3-b4cd-a238af66cdaf	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > SILICATE	1
5855	170	STABLE ISOTOPES	38dadd6d-6adb-44e2-b28a-fd18d797d052	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > STABLE ISOTOPES	1
5856	170	SUSPENDED SOLIDS	718fb499-8c55-4fa6-9a07-ac9155d4bc9d	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > SUSPENDED SOLIDS	1
5857	170	TRACE ELEMENTS	6c320188-da7b-4d52-8e99-57d7ac401841	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > TRACE ELEMENTS	1
5858	171	ADVECTION	0cb7f2c6-5e99-4781-8d4f-19ecbad2e2e0	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > ADVECTION	1
5859	171	BUOY POSITION	81f51367-8467-4183-baea-6b526780fcc7	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > BUOY POSITION	1
5860	171	CONVECTION	10a9c153-f37d-48fe-920d-c790d946ab07	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > CONVECTION	1
5861	171	DIFFUSION	6fe4680b-96e8-4304-ab32-c17a0769932c	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > DIFFUSION	1
5862	171	EDDIES	13927300-c59c-491a-91f3-f1540bcb2d8d	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > EDDIES	1
5863	171	FRESH WATER FLUX	bdd42024-d1a4-4fb2-a16a-06ac0cc1dedc	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > FRESH WATER FLUX	1
5864	171	FRONTS	22b339b5-1af5-46e3-8191-d93729001eeb	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > FRONTS	1
5865	171	GYRES	fc0a6bb2-27f0-48e8-89f1-ebfc7ccd4823	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > GYRES	1
5866	171	OCEAN CURRENTS	510c5f78-e19e-4ce4-b59a-8937aeb84631	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS	1
5867	171	OCEAN MIXED LAYER	48ec6449-373c-41f6-8a61-8f1e9ed95737	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN MIXED LAYER	1
5868	171	THERMOHALINE CIRCULATION	aa1bc71c-daeb-401e-9e29-ebde975482cf	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > THERMOHALINE CIRCULATION	1
5869	171	TURBULENCE	b9f343a1-0b8d-4e88-91bc-21f5d551963f	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > TURBULENCE	1
5870	171	UPWELLING/DOWNWELLING	75ab3537-34b1-4025-b758-7296626079ba	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > UPWELLING/DOWNWELLING	1
5871	171	VORTICITY	55715ed3-471e-46a8-97b6-b463708a2cbe	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > VORTICITY	1
5872	171	WATER MASSES	113edd07-7b1a-4082-b054-b58d3f23b93a	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > WATER MASSES	1
5873	171	WIND-DRIVEN CIRCULATION	03fbea0a-74b9-4c78-8752-a588cff27f17	EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > WIND-DRIVEN CIRCULATION	1
5874	172	ADVECTION	5f6358aa-872c-4c1c-9388-4714138f034a	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > ADVECTION	1
5875	172	BOWEN RATIO	a9b6a001-42b2-48db-b132-62e69f03b8cb	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > BOWEN RATIO	1
5876	172	CONDENSATION	93c1a177-70e3-4c33-a183-baff7f401697	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > CONDENSATION	1
5877	172	CONDUCTION	2ef42281-1e38-4391-b578-ba6a6158f0c2	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > CONDUCTION	1
5878	172	CONVECTION	69d394f7-a792-4a17-8d7f-e60cd60dcda0	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > CONVECTION	1
5879	172	DIFFUSION	064d919e-3262-44c3-a636-8094bc963001	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > DIFFUSION	1
5880	172	EVAPORATION	881eea51-e32c-4174-a73f-d56c94122c2e	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > EVAPORATION	1
5881	172	HEAT FLUX	ee2cb9eb-f960-4e23-9e7c-be64d44a64e7	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > HEAT FLUX	1
5882	172	HEATING RATE	ed2e9f34-2358-4a2a-a83e-febba8989c5c	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > HEATING RATE	1
5883	172	LONGWAVE RADIATION	bc891281-b24c-4310-b39b-81715d7dad08	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > LONGWAVE RADIATION	1
5884	172	REFLECTANCE	d1426df9-7653-442b-8e38-fa28757ec748	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > REFLECTANCE	1
5885	172	SHORTWAVE RADIATION	8d69bce7-efce-4efb-9870-6a6d3a2684fd	EARTH SCIENCE > OCEANS > OCEAN HEAT BUDGET > SHORTWAVE RADIATION	1
5886	173	ABSORPTION	e501d002-d11e-4569-8c0d-e40ae5b45f65	EARTH SCIENCE > OCEANS > OCEAN OPTICS > ABSORPTION	1
5887	173	APHOTIC/PHOTIC ZONE	4e8943e7-daf9-41f2-8a5e-b415b82e6381	EARTH SCIENCE > OCEANS > OCEAN OPTICS > APHOTIC/PHOTIC ZONE	1
5888	173	ATTENUATION/TRANSMISSION	71c78d69-9cfe-48e9-8dd2-9c75acf22283	EARTH SCIENCE > OCEANS > OCEAN OPTICS > ATTENUATION/TRANSMISSION	1
5889	173	BIOLUMINESCENCE	90f97e5b-f883-4a34-a3bc-7dea8d96eb7d	EARTH SCIENCE > OCEANS > OCEAN OPTICS > BIOLUMINESCENCE	1
5890	173	EXTINCTION COEFFICIENTS	5f2ec7b9-3e8c-4d12-bba6-0f84c08729e0	EARTH SCIENCE > OCEANS > OCEAN OPTICS > EXTINCTION COEFFICIENTS	1
5891	173	FLUORESCENCE	a60ae1b6-abfc-4905-8c09-772da7bb1a10	EARTH SCIENCE > OCEANS > OCEAN OPTICS > FLUORESCENCE	1
5892	173	GELBSTOFF	87b074b4-9b73-4e69-b8c0-0f112b1cfa6d	EARTH SCIENCE > OCEANS > OCEAN OPTICS > GELBSTOFF	1
5893	173	IRRADIANCE	40aacf7a-aba0-4ba2-bf85-ea7c39c3322c	EARTH SCIENCE > OCEANS > OCEAN OPTICS > IRRADIANCE	1
5894	173	OCEAN COLOR	78f5a84f-1b5b-44a9-97e7-4a1996cd2e36	EARTH SCIENCE > OCEANS > OCEAN OPTICS > OCEAN COLOR	1
5895	173	OPTICAL DEPTH	001f18d3-7e61-430b-9883-1960c6256fe5	EARTH SCIENCE > OCEANS > OCEAN OPTICS > OPTICAL DEPTH	1
5896	173	PHOTOSYNTHETICALLY ACTIVE RADIATION	b7410899-350a-4443-9430-c7fe1fa3a499	EARTH SCIENCE > OCEANS > OCEAN OPTICS > PHOTOSYNTHETICALLY ACTIVE RADIATION	1
5897	173	RADIANCE	68dacfbb-4f23-4325-b80f-4b09d41bd505	EARTH SCIENCE > OCEANS > OCEAN OPTICS > RADIANCE	1
5898	173	REFLECTANCE	4f7ad022-70ea-4254-b0ae-7a231fc2e46a	EARTH SCIENCE > OCEANS > OCEAN OPTICS > REFLECTANCE	1
5899	173	SCATTERING	20b41061-e6dc-47ef-b73b-00dc08a59618	EARTH SCIENCE > OCEANS > OCEAN OPTICS > SCATTERING	1
5900	173	SECCHI DEPTH	954c2f25-3ec8-4774-ba34-fa4289f33f0e	EARTH SCIENCE > OCEANS > OCEAN OPTICS > SECCHI DEPTH	1
5901	173	TURBIDITY	f0d83687-bc0a-4491-bb3e-697f1018da13	EARTH SCIENCE > OCEANS > OCEAN OPTICS > TURBIDITY	1
5902	173	WATER-LEAVING RADIANCE	ad41b62a-141b-4207-887c-334367860cf4	EARTH SCIENCE > OCEANS > OCEAN OPTICS > WATER-LEAVING RADIANCE	1
5903	174	SEA LEVEL PRESSURE	e5bca08d-ecb3-4b85-8acd-fed782875aa2	EARTH SCIENCE > OCEANS > OCEAN PRESSURE > SEA LEVEL PRESSURE	1
5904	174	WATER PRESSURE	dd025312-0d27-44e0-ae05-7cfcc1aa17f0	EARTH SCIENCE > OCEANS > OCEAN PRESSURE > WATER PRESSURE	1
5905	175	OCEAN MIXED LAYER	64074461-95d0-4538-869a-0114e39216aa	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > OCEAN MIXED LAYER	1
5906	175	POTENTIAL TEMPERATURE	e02b0b50-a0f2-4c47-841b-9689fdb99121	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > POTENTIAL TEMPERATURE	1
5907	175	SEA SURFACE TEMPERATURE	bd24a9a9-7d52-4c29-b2a0-6cefd216ae78	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE	1
5908	175	THERMOCLINE	68772b70-e493-48d5-b063-00b9d2dd4078	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > THERMOCLINE	1
5909	175	WATER TEMPERATURE	46206e8c-8def-406f-9e62-da4e74633a58	EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > WATER TEMPERATURE	1
5910	176	GRAVITY WAVES	dc9fcd27-58ac-4705-a522-6475d59cfb81	EARTH SCIENCE > OCEANS > OCEAN WAVES > GRAVITY WAVES	1
5911	176	ROSSBY/PLANETARY WAVES	41764af0-1264-4adb-881d-44991489344c	EARTH SCIENCE > OCEANS > OCEAN WAVES > ROSSBY/PLANETARY WAVES	1
5912	176	SEA STATE	11aca777-8a01-42ce-b076-b3059c3d8cae	EARTH SCIENCE > OCEANS > OCEAN WAVES > SEA STATE	1
5913	176	SEICHES	2b4963ba-1a7a-419d-97ef-eacaa14688e0	EARTH SCIENCE > OCEANS > OCEAN WAVES > SEICHES	1
5914	176	SIGNIFICANT WAVE HEIGHT	1ac6850e-9266-4e90-ba83-b6a6cc4ae365	EARTH SCIENCE > OCEANS > OCEAN WAVES > SIGNIFICANT WAVE HEIGHT	1
5915	176	STORM SURGE	0bf50cd4-8a97-468c-8e73-047e3e09a03d	EARTH SCIENCE > OCEANS > OCEAN WAVES > STORM SURGE	1
5916	176	SURF BEAT	a90526a9-5476-45bc-9a15-73ac2dfc62ab	EARTH SCIENCE > OCEANS > OCEAN WAVES > SURF BEAT	1
5917	176	SWELLS	4e4d3c18-cdd4-474a-a936-6e127ec526f7	EARTH SCIENCE > OCEANS > OCEAN WAVES > SWELLS	1
5918	176	TOPOGRAPHIC WAVES	3dd99ea6-51bd-4b78-bf2e-d5aeca7f5bc8	EARTH SCIENCE > OCEANS > OCEAN WAVES > TOPOGRAPHIC WAVES	1
5919	176	TSUNAMIS	7a79a3f3-1817-4c9f-8485-550a022b5a8d	EARTH SCIENCE > OCEANS > OCEAN WAVES > TSUNAMIS	1
5920	176	WAVE FETCH	09b326df-79b3-41b8-8998-e06344b0fe0d	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE FETCH	1
5921	176	WAVE FREQUENCY	0d91f6d9-44c4-4418-90b0-00feb09c6fc0	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE FREQUENCY	1
5922	176	WAVE HEIGHT	0fc68280-1361-43e1-bc5a-40c49e9679b7	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE HEIGHT	1
5923	176	WAVE LENGTH	5daa972e-b47c-4050-97f1-1e628401fb97	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE LENGTH	1
5924	176	WAVE OVERTOPPING	5377fb64-b10a-4284-9b7b-be77b4c16fe5	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE OVERTOPPING	1
5925	176	WAVE PERIOD	99ea6719-b751-4a4f-95d4-aaa02e961bc1	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD	1
5926	176	WAVE RUNUP	9a4816c1-dba8-4ae4-9c3b-7f98a4ac245b	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE RUNUP	1
5927	176	WAVE SETUP	4dd520ea-30fc-416d-b98c-340fd23431d3	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SETUP	1
5928	176	WAVE SPECTRA	e79ff727-c598-4a1c-8b4f-b6019fcf386b	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA	1
5929	176	WAVE SPEED/DIRECTION	e52114b2-adbc-4e3e-9c87-1a7f245fe5ef	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPEED/DIRECTION	1
5930	176	WAVE TYPES	a4f0e0d2-4bcb-4675-b874-e6e0f3a8c462	EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE TYPES	1
5931	176	WIND WAVES	0c9adb35-b203-42d7-8ccf-b7f2079db7ce	EARTH SCIENCE > OCEANS > OCEAN WAVES > WIND WAVES	1
5932	177	CONVERGENCE/DIVERGENCE	b59e188c-49b8-41b3-94c4-0bc1dbb554fe	EARTH SCIENCE > OCEANS > OCEAN WINDS > CONVERGENCE/DIVERGENCE	1
5933	177	SURFACE WINDS	fbc53539-ce4e-4e3e-bbd2-8270386616b4	EARTH SCIENCE > OCEANS > OCEAN WINDS > SURFACE WINDS	1
5934	177	TURBULENCE	13aeaea0-ab45-4148-abcf-c6becf7a8934	EARTH SCIENCE > OCEANS > OCEAN WINDS > TURBULENCE	1
5935	177	VERTICAL WIND MOTION	ab1e152c-eab9-400a-a90f-15cb64ed2a75	EARTH SCIENCE > OCEANS > OCEAN WINDS > VERTICAL WIND MOTION	1
5936	177	VORTICITY	253ccaf2-dd4c-4fc1-923d-1aea542a51b0	EARTH SCIENCE > OCEANS > OCEAN WINDS > VORTICITY	1
5937	177	WIND CHILL	d571e1f5-7449-4052-943b-94d76f762677	EARTH SCIENCE > OCEANS > OCEAN WINDS > WIND CHILL	1
5938	177	WIND SHEAR	855c22f5-d1e0-4ccf-81bd-c8120e7c4055	EARTH SCIENCE > OCEANS > OCEAN WINDS > WIND SHEAR	1
5939	177	WIND STRESS	91d73256-925d-4d04-9b55-aaf088080cac	EARTH SCIENCE > OCEANS > OCEAN WINDS > WIND STRESS	1
5940	178	CONDUCTIVITY	7041e51c-e2de-405a-b154-6016f624f54f	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > CONDUCTIVITY	1
5941	178	DENSITY	007ab607-2ee1-484d-85fb-0bfb89f18c9b	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > DENSITY	1
5942	178	DESALINIZATION	41926d67-161a-4add-bb12-66038c919efb	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > DESALINIZATION	1
5943	178	HALOCLINE	04305c55-14f0-42a3-a099-79eb326946d7	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > HALOCLINE	1
5944	178	POTENTIAL DENSITY	fe4a246b-4614-422b-8ca5-0481ee417318	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > POTENTIAL DENSITY	1
5945	178	PYCNOCLINE	2ad73f85-8bad-4e5a-a902-e83eee910b5e	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > PYCNOCLINE	1
5946	178	SALINITY	7e95b5fc-1d58-431a-af36-948b29fa870d	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > SALINITY	1
5947	178	SALT TRANSPORT	15f87fbc-b972-403f-97c0-15f387a13efe	EARTH SCIENCE > OCEANS > SALINITY/DENSITY > SALT TRANSPORT	1
5948	179	HEAT FLUX	ae1c9b54-caf2-4726-b180-5c6544f09111	EARTH SCIENCE > OCEANS > SEA ICE > HEAT FLUX	1
5949	179	ICE DEFORMATION	3cdebef6-902d-4c1a-9d7e-7609f8ee6ef6	EARTH SCIENCE > OCEANS > SEA ICE > ICE DEFORMATION	1
5950	179	ICE DEPTH/THICKNESS	a735d8ca-182c-4307-9305-186a065e84a4	EARTH SCIENCE > OCEANS > SEA ICE > ICE DEPTH/THICKNESS	1
5951	179	ICE EDGES	f0cd20bd-41e8-4ca0-9ae3-7c602c251858	EARTH SCIENCE > OCEANS > SEA ICE > ICE EDGES	1
5952	179	ICE EXTENT	87feb47e-aee3-42f1-8c39-5109d9d5422e	EARTH SCIENCE > OCEANS > SEA ICE > ICE EXTENT	1
5953	179	ICE FLOES	aa15804c-5f7f-40cc-b949-aa3e4418fc27	EARTH SCIENCE > OCEANS > SEA ICE > ICE FLOES	1
5954	179	ICE GROWTH/MELT	89fc22ca-326e-468c-ad3d-171c4ad34977	EARTH SCIENCE > OCEANS > SEA ICE > ICE GROWTH/MELT	1
5955	179	ICE ROUGHNESS	a6c3e78f-f408-4b72-941a-f40e3d83dd60	EARTH SCIENCE > OCEANS > SEA ICE > ICE ROUGHNESS	1
5956	179	ICE TEMPERATURE	2a664e2d-4e50-463a-af9f-b14b86eb42a7	EARTH SCIENCE > OCEANS > SEA ICE > ICE TEMPERATURE	1
5957	179	ICE TYPES	f5d7cafc-13bf-4ec8-bc6e-a6d850fae5c8	EARTH SCIENCE > OCEANS > SEA ICE > ICE TYPES	1
5958	179	ICEBERGS	1151dc7e-7441-4a21-95b6-1d03a1053f60	EARTH SCIENCE > OCEANS > SEA ICE > ICEBERGS	1
5959	179	ISOTOPES	9d99408d-0d8b-4642-a2cb-edee8319fe1d	EARTH SCIENCE > OCEANS > SEA ICE > ISOTOPES	1
5960	179	LEADS	f523f73f-efcc-4193-b9e3-1161ed7f4881	EARTH SCIENCE > OCEANS > SEA ICE > LEADS	1
5961	179	PACK ICE	ea85ea0b-1b7d-464a-9f8c-1f80383ffc51	EARTH SCIENCE > OCEANS > SEA ICE > PACK ICE	1
5962	179	POLYNYAS	10a128a6-12d4-4bce-b25d-2ffc464182f4	EARTH SCIENCE > OCEANS > SEA ICE > POLYNYAS	1
5963	179	REFLECTANCE	8ed9f39d-986e-4b36-83f9-f29f6a4df89b	EARTH SCIENCE > OCEANS > SEA ICE > REFLECTANCE	1
5964	179	SALINITY	04fa9023-ab68-4dd0-a82e-abe685105a53	EARTH SCIENCE > OCEANS > SEA ICE > SALINITY	1
5965	179	SEA ICE AGE	b6085d71-a7ee-4b65-9c9c-ff374bdc3974	EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE AGE	1
5966	179	SEA ICE CONCENTRATION	bb27bbb7-7bc4-4e38-833a-30e0a7861ccc	EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE CONCENTRATION	1
5967	179	SEA ICE ELEVATION	6e2f1371-05b1-41db-a6d9-bccd7cc2b3da	EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE ELEVATION	1
5968	179	SEA ICE MOTION	a47ab696-7ed9-4374-8965-c8996e61463d	EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE MOTION	1
5969	179	SNOW DEPTH	5575125b-7f15-4d46-ba47-f86de96a1a25	EARTH SCIENCE > OCEANS > SEA ICE > SNOW DEPTH	1
5970	179	SNOW MELT	32259124-81f7-4845-b2fb-6435d7bb5804	EARTH SCIENCE > OCEANS > SEA ICE > SNOW MELT	1
5971	180	SEA SURFACE HEIGHT	5c0b448c-7eb4-4e8c-8403-260cbb6114bb	EARTH SCIENCE > OCEANS > SEA SURFACE TOPOGRAPHY > SEA SURFACE HEIGHT	1
5972	180	SEA SURFACE SLOPE	52a32bd3-d701-49e1-a827-67b3d96d8e56	EARTH SCIENCE > OCEANS > SEA SURFACE TOPOGRAPHY > SEA SURFACE SLOPE	1
5973	181	STORM SURGE	062be713-9c35-458e-86e2-26cea9415f5d	EARTH SCIENCE > OCEANS > TIDES > STORM SURGE	1
5974	181	TIDAL COMPONENTS	f4f40ec7-e698-4e11-b406-a0fa7f4b530c	EARTH SCIENCE > OCEANS > TIDES > TIDAL COMPONENTS	1
5975	181	TIDAL CURRENTS	54ab2e0e-8e36-48e8-b020-ea9a5b453373	EARTH SCIENCE > OCEANS > TIDES > TIDAL CURRENTS	1
5976	181	TIDAL HEIGHT	9afcf69c-f56f-45a9-afd9-6f929850326b	EARTH SCIENCE > OCEANS > TIDES > TIDAL HEIGHT	1
5977	181	TIDAL RANGE	a5a6266a-9457-4acf-b140-fcdc8bc00a00	EARTH SCIENCE > OCEANS > TIDES > TIDAL RANGE	1
5978	182	OCEAN CONTAMINANTS	f1ee3e81-09b9-48d4-81d9-5faeb90430cc	EARTH SCIENCE > OCEANS > WATER QUALITY > OCEAN CONTAMINANTS	1
5979	183	CALCIUM	7b9fb947-97cd-4354-a799-f14a81564132	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > CALCIUM	1
5980	183	CARBON DIOXIDE	37dac8df-b04b-4561-91fb-886e1bded2c1	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > CARBON DIOXIDE	1
5981	183	ELECTRICAL PROPERTIES	01a4a324-cad3-441d-b0f1-02dc9742784a	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > ELECTRICAL PROPERTIES	1
5982	183	ICE CORE AIR BUBBLES	3643618f-3af3-4c69-8beb-2ad14141a176	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > ICE CORE AIR BUBBLES	1
5983	183	IONS	591d2038-5c5e-47bf-a551-1b28f33d1f05	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > IONS	1
5984	183	IRON	cf32d0f2-31f5-450d-9f1d-8aa38fd526dc	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > IRON	1
5985	183	ISOTOPES	096f466a-a86a-42ac-93f7-05a799910817	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > ISOTOPES	1
5986	183	METHANE	daab3b2a-1fe7-4ad9-8340-1a7cfa54a2ac	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > METHANE	1
5987	183	NITROUS OXIDE	ddbd1be1-2a1b-4aea-a085-6a63208a75c0	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > NITROUS OXIDE	1
5988	183	PARTICULATE MATTER	63c7d604-707e-4c38-8baf-19a620e61917	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > PARTICULATE MATTER	1
5989	183	POTASSIUM	aeaa43ab-5ccf-4df7-b8ad-b9f9f4249551	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > POTASSIUM	1
5990	183	SODIUM	c692e8e4-b920-4eb5-86c3-b5f6121fec4b	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > SODIUM	1
5991	183	VELOCITY	4487cb97-df49-421f-8c00-5c5f12dd8af1	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > VELOCITY	1
5992	183	VOLCANIC DEPOSITS	2f4ccb5c-7b99-442c-9054-964070d95f7b	EARTH SCIENCE > PALEOCLIMATE > ICE CORE RECORDS > VOLCANIC DEPOSITS	1
5993	184	BOREHOLES	5a63fa7f-2971-4874-a920-394df07d218e	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > BOREHOLES	1
5994	184	CAVE DEPOSITS	1651d2e2-4483-42fc-aef2-fd49e650eff1	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > CAVE DEPOSITS	1
5995	184	GLACIATION	8c615709-df55-4b09-a5a9-1fabb133fe1a	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > GLACIATION	1
5996	184	ISOTOPES	61f57065-8f47-45c7-8319-f6115153a6ad	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > ISOTOPES	1
5997	184	LOESS	733234ec-053b-4595-811a-b221e6afb35e	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > LOESS	1
5998	184	MACROFOSSILS	d412deec-d4ef-4c97-ac1c-f92ddb6964c6	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > MACROFOSSILS	1
5999	184	MICROFOSSILS	98e15316-0055-4392-8825-c38f447d6582	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > MICROFOSSILS	1
6000	184	PALEOMAGNETIC DATA	f2ceb98b-4b5d-4ee6-b033-e987d2f820f1	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > PALEOMAGNETIC DATA	1
6001	184	PALEOSOLS	b54e01eb-02d9-413a-baf1-40a6e59d9eae	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > PALEOSOLS	1
6002	184	PALEOVEGETATION	e4871f3e-bc88-4380-b7b7-3a18afccc2bd	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > PALEOVEGETATION	1
6003	184	POLLEN	14c8721e-4d05-4aaa-90be-8607ae2f84b1	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > POLLEN	1
6004	184	RADIOCARBON	bf0db125-0182-42e7-81c9-6ed55a05ddd0	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > RADIOCARBON	1
6005	184	SEDIMENTS	858d3f93-f2eb-4d2a-87c5-68018f206a47	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > SEDIMENTS	1
6006	184	STRATIGRAPHIC SEQUENCE	ac45c059-9555-45ee-ad20-d58514578f1e	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > STRATIGRAPHIC SEQUENCE	1
6007	184	TREE RINGS	84510f18-a4e6-434c-a54c-44cc995e1af2	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > TREE RINGS	1
6008	184	VOLCANIC DEPOSITS	9761565c-2126-49cd-b4c4-cd3bcb5dbbde	EARTH SCIENCE > PALEOCLIMATE > LAND RECORDS > VOLCANIC DEPOSITS	1
6009	185	BOREHOLES	e001c431-c204-419e-af64-cc8978132abf	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > BOREHOLES	1
6010	185	CORAL DEPOSITS	296b7bc4-c031-48ea-bb6d-99f7c971c953	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > CORAL DEPOSITS	1
6011	185	ISOTOPES	56589fec-7573-42df-b853-2754cdc9e1b7	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > ISOTOPES	1
6012	185	LAKE LEVELS	77cbdebf-eddf-42b5-8603-e939eccd1780	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > LAKE LEVELS	1
6013	185	MACROFOSSILS	f986b716-d26c-4c98-8166-b415229186ff	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > MACROFOSSILS	1
6014	185	MICROFOSSILS	6e872413-f416-43dd-a960-942ef892ae59	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > MICROFOSSILS	1
6015	185	OXYGEN ISOTOPES	a65ec029-86a7-4c3b-b2b3-ee26353aaf36	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > OXYGEN ISOTOPES	1
6016	185	PALEOMAGNETIC DATA	d42bf3e3-3eda-471a-adb5-ddf1240cd474	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > PALEOMAGNETIC DATA	1
6017	185	POLLEN	adcd37fe-9f4a-4d8d-8f79-489775707ea2	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > POLLEN	1
6018	185	RADIOCARBON	23822618-39a2-4b2b-9162-37bb0651c118	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > RADIOCARBON	1
6019	185	SEDIMENTS	d324729f-cc0d-4943-8d1a-d38335120c00	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > SEDIMENTS	1
6020	185	STRATIGRAPHIC SEQUENCE	4722fc1e-f93f-4aa1-854a-2b8a82920008	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > STRATIGRAPHIC SEQUENCE	1
6021	185	VARVE DEPOSITS	4ad60c3b-f72e-4f54-9d3e-0048373c166d	EARTH SCIENCE > PALEOCLIMATE > OCEAN/LAKE RECORDS > VARVE DEPOSITS	1
6022	186	AIR TEMPERATURE RECONSTRUCTION	cb49a2e7-bd89-4d3a-974a-8776a763a4ae	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > AIR TEMPERATURE RECONSTRUCTION	1
6023	186	ATMOSPHERIC CIRCULATION RECONSTRUCTION	2bdfbf06-c583-4e51-a595-dbc6143d95e0	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > ATMOSPHERIC CIRCULATION RECONSTRUCTION	1
6024	186	DROUGHT/PRECIPITATION RECONSTRUCTION	cc063daf-1db5-4597-9de2-0501a5593947	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > DROUGHT/PRECIPITATION RECONSTRUCTION	1
6025	186	GROUND WATER RECONSTRUCTION	cf0e53d3-c8ae-4baa-8a31-672a2252f285	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > GROUND WATER RECONSTRUCTION	1
6026	186	LAKE LEVEL RECONSTRUCTION	fed291ec-8f7d-4131-a5cd-dc04706f61b0	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > LAKE LEVEL RECONSTRUCTION	1
6027	186	OCEAN SALINITY RECONSTRUCTION	80a6803a-5bf3-4439-b13f-0909e0ea40f9	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > OCEAN SALINITY RECONSTRUCTION	1
6028	186	SEA LEVEL RECONSTRUCTION	e240565d-d265-474b-a25b-34059526ae44	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > SEA LEVEL RECONSTRUCTION	1
6029	186	SEA SURFACE TEMPERATURE RECONSTRUCTION	e7b30694-5d05-404b-9748-b8f6adc3491d	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > SEA SURFACE TEMPERATURE RECONSTRUCTION	1
6030	186	SOLAR FORCING/INSOLATION RECONSTRUCTION	4f07a511-1c78-4b2b-8c6a-f4aeedb0f5b6	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > SOLAR FORCING/INSOLATION RECONSTRUCTION	1
6031	186	STREAMFLOW RECONSTRUCTION	7859191e-732b-47cf-b1a3-fc7a934509ce	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > STREAMFLOW RECONSTRUCTION	1
6032	186	VEGETATION RECONSTRUCTION	91600c9b-397e-4855-b21e-b9e97e6d5261	EARTH SCIENCE > PALEOCLIMATE > PALEOCLIMATE RECONSTRUCTIONS > VEGETATION RECONSTRUCTION	1
6033	187	HYDROGEN GAS	96bbae63-81c1-43b4-90f0-52731e2b52ca	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > HYDROGEN GAS	1
6034	187	NATURAL GAS	72eb280a-d5d0-4c5e-b789-8f1a8cf8bdac	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > NATURAL GAS	1
6035	187	PETROLEUM	44d0ad8f-fe22-4d17-bc47-c0b728a82baf	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > PETROLEUM	1
6036	187	RECLAMATION/REVEGETATION/RESTORATION	4add3005-9151-4b8d-a0bc-14c3908ef3a9	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > RECLAMATION/REVEGETATION/RESTORATION	1
6037	188	BIOGEOCHEMICAL PROCESSES	b472632f-8e67-4892-9896-1c14c5089682	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > BIOGEOCHEMICAL PROCESSES	1
6038	188	GEOCHEMICAL PROCESSES	e6fb1b81-8ffc-486f-b1a1-2f292af8cee6	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES	1
6039	188	GEOCHEMICAL PROPERTIES	048df94e-841d-4f4d-a5c5-6683d1d07aa6	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES	1
6040	188	MARINE GEOCHEMICAL PROCESSES	5cef2f41-a17a-4eff-8ce4-328593e1b703	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > MARINE GEOCHEMICAL PROCESSES	1
6041	189	COORDINATE REFERENCE SYSTEM	14b19e68-0fb3-43b1-a102-537c4e33c338	EARTH SCIENCE > SOLID EARTH > GEODETICS > COORDINATE REFERENCE SYSTEM	1
6042	189	ELLIPSOID CHARACTERISTICS	bc640e63-70c1-4228-b2dc-6aa1ac6edfa6	EARTH SCIENCE > SOLID EARTH > GEODETICS > ELLIPSOID CHARACTERISTICS	1
6043	189	GEOID CHARACTERISTICS	6bbbf7b0-434b-4dbc-9fe8-e5e31fe99614	EARTH SCIENCE > SOLID EARTH > GEODETICS > GEOID CHARACTERISTICS	1
6044	190	ELECTRICAL FIELD	3202dab6-144a-4bfb-9bda-9d07e5ee7ec2	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > ELECTRICAL FIELD	1
6045	190	GEOMAGNETIC FORECASTS	02290e22-24ae-40f6-96f1-0c6c76a145af	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC FORECASTS	1
6046	190	GEOMAGNETIC INDICES	ae35f430-6534-49de-8b4c-edfc1e98870a	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES	1
6047	190	MAGNETIC FIELD	204b482b-449b-42c9-a5bb-f6da42bee3a4	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD	1
6048	190	PALEOMAGNETISM	720969dd-e966-41aa-af94-ee41cdf60390	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > PALEOMAGNETISM	1
6049	190	REFERENCE FIELDS	fd631e31-fe6f-462e-a3f6-c07b4b736ac7	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > REFERENCE FIELDS	1
6050	191	AEOLIAN LANDFORMS	26637389-f4f6-47a0-9c3d-17e93ab99dea	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS	1
6051	191	AEOLIAN PROCESSES	f15b2ad3-f658-420b-99b4-41588646d9b7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES	1
6052	191	COASTAL LANDFORMS	c58320e6-3f1d-4c36-9bee-6bad73404c21	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS	1
6053	191	COASTAL PROCESSES	672d6958-4bbc-4b33-adc8-927e4348908b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES	1
6054	191	FLUVIAL LANDFORMS	cb5193ab-2d7a-4b35-b7ec-f16ce78ae270	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS	1
6055	191	FLUVIAL PROCESSES	6f47ae88-f28f-43e3-be6a-34f86b15fe19	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES	1
6056	195	EARTHQUAKES	601d36fc-8171-475c-a1c5-84802aecb77e	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES	1
6057	191	GLACIAL LANDFORMS	3c78951a-0293-4fb0-baff-ec7372fe784d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS	1
6058	191	GLACIAL PROCESSES	d7b62912-5970-46b1-be45-6a603c9a6979	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES	1
6059	191	KARST LANDFORMS	ac2d1035-1896-42c1-861b-042a917b6889	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS	1
6060	191	KARST PROCESSES	63846997-4a3f-41e1-9241-6d5053360d7a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES	1
6061	191	TECTONIC LANDFORMS	46172bbe-8bf0-49a0-848f-129c089aeb8e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS	1
6062	191	TECTONIC PROCESSES	f0bd7eeb-9004-4e40-a649-f6010d8a4303	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES	1
6063	192	GEOTHERMAL ENERGY	33d1810f-40c6-4b37-ac90-7435ef5fa507	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL ENERGY	1
6064	192	GEOTHERMAL TEMPERATURE	cacfd8f0-b83a-46b7-b324-52ce1b55baa9	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL TEMPERATURE	1
6065	193	CONTROL SURVEYS	8b39b880-f385-4dab-a563-24064b43be7e	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > CONTROL SURVEYS	1
6066	193	CRUSTAL MOTION	122f7d15-7e5c-4249-992c-c753c80cf05b	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > CRUSTAL MOTION	1
6067	193	GRAVITATIONAL FIELD	56b4cbe5-e5f7-4e61-8c48-bbb858b505e6	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > GRAVITATIONAL FIELD	1
6068	193	GRAVITY ANOMALIES	fb7eeee0-9ad1-40f8-baa2-df7dc3acb6d3	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > GRAVITY ANOMALIES	1
6069	193	GRAVITY	69af3046-08e0-4c24-981d-803c0412ce58	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > GRAVITY	1
6070	193	POLAR MOTION	c44b078d-ec95-47d5-9a43-ba8475e568d2	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > POLAR MOTION	1
6071	193	ROTATIONAL MOTION/VARIATIONS	05225982-60ab-4772-a0b7-f67c3b853ab9	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > ROTATIONAL MOTION/VARIATIONS	1
6072	193	SATELLITE ORBITS/REVOLUTION	71278ba7-9a13-43ba-9ec3-62ae2b39de88	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION	1
6073	194	AGE DETERMINATIONS	d4ac49a1-9ba5-4a90-a033-2ef317028352	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > AGE DETERMINATIONS	1
6074	194	BEDROCK LITHOLOGY	4beaeec9-0750-44e6-8fb4-8d0085efc82e	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > BEDROCK LITHOLOGY	1
6075	194	ELEMENTS	da22144c-634d-4007-aba9-e636a9f2fa3f	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > ELEMENTS	1
6076	194	GAS HYDRATES	a654a922-8b69-46f2-be40-d4d830ce999c	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES	1
6077	194	IGNEOUS ROCKS	e8d97ffd-2fd2-4989-88a7-9772fc9b7cd8	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS	1
6078	194	METALS	7b76bca5-32ee-4285-8550-0de120b01a13	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS	1
6079	194	METAMORPHIC ROCKS	d220bbb1-410e-4b77-9663-78cb68c6b134	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS	1
6080	194	METEORITES	96be1efc-d5e2-423d-8ade-00b3d454244d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES	1
6081	195	NEOTECTONICS	3ef98fe3-3471-414b-8b8c-e88d43c6aeaf	EARTH SCIENCE > SOLID EARTH > TECTONICS > NEOTECTONICS	1
6082	194	MINERALS	387a51ad-382f-4297-be72-fdd4bb0fe3f9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS	1
6083	194	NON-METALLIC MINERALS	d64a9627-3cf8-41d3-aaf7-8c2c46fb4a13	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS	1
6084	194	SEDIMENTARY ROCKS	85353d7b-05d8-4c32-a5b2-065f1f22f026	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS	1
6085	194	SEDIMENTS	6600ace1-fc1e-4b5a-9f82-0afa19acf037	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTS	1
6086	195	CORE PROCESSES	57503db6-7cff-4e92-bcac-1ba2c3c0cb48	EARTH SCIENCE > SOLID EARTH > TECTONICS > CORE PROCESSES	1
6087	195	PLATE TECTONICS	71e9bc66-6f8c-41ec-8b22-2fe390223639	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS	1
6088	195	VOLCANIC ACTIVITY	1faaede0-2cd6-4447-b28b-0a28d9e2d067	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY	1
6089	196	GAMMA RAY FLUX	fd8d9257-795c-4406-b205-cf20059d8e77	EARTH SCIENCE > SPECTRAL/ENGINEERING > GAMMA RAY > GAMMA RAY FLUX	1
6090	197	BRIGHTNESS TEMPERATURE	73629546-592e-41ed-bfde-feb4c94415fb	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > BRIGHTNESS TEMPERATURE	1
6091	197	INFRARED FLUX	d76e6734-956b-419d-9d7a-52b8e645b6ac	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > INFRARED FLUX	1
6092	197	INFRARED IMAGERY	d1407646-e34a-4a43-ae1d-afc4c229d6de	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > INFRARED IMAGERY	1
6093	197	INFRARED RADIANCE	69f475b6-42af-4822-ae57-6c8fd8ebad4a	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > INFRARED RADIANCE	1
6094	197	REFLECTED INFRARED	ff985037-2f20-4b08-bb22-3ed701ed2f4d	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > REFLECTED INFRARED	1
6095	197	SENSOR COUNTS	32212cbf-e2ba-44c9-930c-8b454ea88bee	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > SENSOR COUNTS	1
6096	197	THERMAL INFRARED	68c2baba-b9b9-41d4-89bf-07488728bc4f	EARTH SCIENCE > SPECTRAL/ENGINEERING > INFRARED WAVELENGTHS > THERMAL INFRARED	1
6097	198	LIDAR BACKSCATTER	ca776e14-fc3d-4044-9d1a-fd7c07569399	EARTH SCIENCE > SPECTRAL/ENGINEERING > LIDAR > LIDAR BACKSCATTER	1
6098	198	LIDAR DEPOLARIZATION RATIO	19c3f401-1328-495c-9705-74b0175fee56	EARTH SCIENCE > SPECTRAL/ENGINEERING > LIDAR > LIDAR DEPOLARIZATION RATIO	1
6099	199	ANTENNA TEMPERATURE	570397b4-3b45-4e12-85c3-ef26779a2c96	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > ANTENNA TEMPERATURE	1
6100	199	BRIGHTNESS TEMPERATURE	d8525750-2ca4-4b1f-a717-08fda61fd547	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > BRIGHTNESS TEMPERATURE	1
6101	199	MICROWAVE IMAGERY	af234b68-d1ad-40ea-aa1b-6bc2c8e5b467	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > MICROWAVE IMAGERY	1
6102	199	MICROWAVE RADIANCE	d9654ddc-1dc0-4f9d-9b95-61ab0c3d6f87	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > MICROWAVE RADIANCE	1
6103	199	SENSOR COUNTS	5f6e0ca7-5d60-4973-890b-08ad82654331	EARTH SCIENCE > SPECTRAL/ENGINEERING > MICROWAVE > SENSOR COUNTS	1
6104	200	AIRSPEED/GROUND SPEED	7ebe88d4-fa73-4dd1-8cbd-6b1c266dff52	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > AIRSPEED/GROUND SPEED	1
6105	200	ATTITUDE CHARACTERISTICS	edbca82e-9396-4842-ad91-18c0000b2741	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > ATTITUDE CHARACTERISTICS	1
6106	200	DATA SYNCHRONIZATION TIME	762f9d7f-5f2d-423d-81c4-288350f64b9d	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > DATA SYNCHRONIZATION TIME	1
6107	200	FLIGHT DATA LOGS	6b68bae6-e5cb-44ff-ad40-a8100a88e5b1	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > FLIGHT DATA LOGS	1
6108	200	LINE OF SIGHT VELOCITY	53ab7819-1837-4919-b4a8-85bcc8b7731c	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > LINE OF SIGHT VELOCITY	1
6109	200	ORBITAL CHARACTERISTICS	4809f1e1-1b36-46a7-a7ae-ce55523424e6	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > ORBITAL CHARACTERISTICS	1
6110	200	VIEWING GEOMETRY	d622004f-e155-4af3-87c5-61b3a4b87692	EARTH SCIENCE > SPECTRAL/ENGINEERING > PLATFORM CHARACTERISTICS > VIEWING GEOMETRY	1
6111	201	DOPPLER VELOCITY	5d6377ee-def2-4457-b780-6bcb202d7e3e	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > DOPPLER VELOCITY	1
6112	201	MEAN RADIAL VELOCITY	bb20786b-2499-40b0-a9a5-2cc64421a6d2	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > MEAN RADIAL VELOCITY	1
6113	201	RADAR BACKSCATTER	625da982-3648-43fc-a640-1b230509944e	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER	1
6114	201	RADAR CROSS-SECTION	9613f08d-da11-4ed0-989e-c0c830870044	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR CROSS-SECTION	1
6115	201	RADAR IMAGERY	53f69037-ff05-4b09-a95d-e65ff42da595	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY	1
6116	201	RADAR REFLECTIVITY	46975e66-863a-49c9-b673-b2e099a04c85	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR REFLECTIVITY	1
6117	201	RETURN POWER	6eca12d1-bafd-448c-bdce-a4438efb359e	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RETURN POWER	1
6118	201	SENSOR COUNTS	e2c01004-be17-4be4-bfcd-7b5c7fc958d6	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > SENSOR COUNTS	1
6119	201	SIGMA NAUGHT	11e14ac8-e9f3-4737-b83d-98668ad975ed	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > SIGMA NAUGHT	1
6120	201	SPECTRUM WIDTH	41a7f02b-5ab6-4c1e-8583-abb870507ea1	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > SPECTRUM WIDTH	1
6121	202	RADIO WAVE FLUX	b3578efe-fc86-4fb0-92b5-42c08bae5e3c	EARTH SCIENCE > SPECTRAL/ENGINEERING > RADIO WAVE > RADIO WAVE FLUX	1
6122	203	DOME TEMPERATURE	68ac1c78-6b8b-4e45-b588-38ff94ceb3a4	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > DOME TEMPERATURE	1
6123	203	ELECTRICAL PROPERTIES	914a7dba-82ae-4419-97cf-397007ad9c30	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > ELECTRICAL PROPERTIES	1
6124	203	GEOLOCATION	7a0ab5f9-2317-4217-a081-8d4a46eb5334	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > GEOLOCATION	1
6125	203	PHASE AND AMPLITUDE	a4a3d233-581b-4171-bf16-41a1528a7dda	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > PHASE AND AMPLITUDE	1
6126	203	SINK TEMPERATURE	4a42042b-7427-4cf2-9475-7d1788e3ac54	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > SINK TEMPERATURE	1
6127	203	THERMAL PROPERTIES	7d3d6c15-b328-43a4-92eb-7d3c430647c4	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > THERMAL PROPERTIES	1
6128	203	TOTAL PRESSURE	733092b1-4256-433a-85fe-78c912f21f80	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > TOTAL PRESSURE	1
6129	203	TOTAL TEMPERATURE	3ef1cc7b-2864-46e3-b399-fcc1fbcf0d9b	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > TOTAL TEMPERATURE	1
6130	203	ULTRAVIOLET SENSOR TEMPERATURE	36085074-ba97-450b-847b-046509b0e09a	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > ULTRAVIOLET SENSOR TEMPERATURE	1
6131	203	VIEWING GEOMETRY	14edbe59-89a4-45ce-ac61-0143fb311da6	EARTH SCIENCE > SPECTRAL/ENGINEERING > SENSOR CHARACTERISTICS > VIEWING GEOMETRY	1
6132	204	SENSOR COUNTS	03d45804-cc21-449d-81f4-4bb778f97ac6	EARTH SCIENCE > SPECTRAL/ENGINEERING > ULTRAVIOLET WAVELENGTHS > SENSOR COUNTS	1
6133	204	ULTRAVIOLET FLUX	01e4b433-34ae-4ffb-a73b-dff7ae4c789a	EARTH SCIENCE > SPECTRAL/ENGINEERING > ULTRAVIOLET WAVELENGTHS > ULTRAVIOLET FLUX	1
6134	204	ULTRAVIOLET RADIANCE	ca87e2c2-9087-42f7-a88a-93ace50ebe39	EARTH SCIENCE > SPECTRAL/ENGINEERING > ULTRAVIOLET WAVELENGTHS > ULTRAVIOLET RADIANCE	1
6135	205	SENSOR COUNTS	a3792ab1-61af-48be-acf2-116c291a3765	EARTH SCIENCE > SPECTRAL/ENGINEERING > VISIBLE WAVELENGTHS > SENSOR COUNTS	1
6136	205	VISIBLE FLUX	7971f416-cf75-47f4-9108-6184baab58e5	EARTH SCIENCE > SPECTRAL/ENGINEERING > VISIBLE WAVELENGTHS > VISIBLE FLUX	1
6137	205	VISIBLE IMAGERY	03f0c0a3-04a7-4ef8-8ec0-3c2266510815	EARTH SCIENCE > SPECTRAL/ENGINEERING > VISIBLE WAVELENGTHS > VISIBLE IMAGERY	1
6138	205	VISIBLE RADIANCE	b590bfda-a053-4439-8f86-a2811e67ce46	EARTH SCIENCE > SPECTRAL/ENGINEERING > VISIBLE WAVELENGTHS > VISIBLE RADIANCE	1
6139	206	X-RAY FLUX	e32b5dca-c243-40d8-9e06-d146a40a71df	EARTH SCIENCE > SPECTRAL/ENGINEERING > X-RAY > X-RAY FLUX	1
6140	207	AURORAE	792cf9f0-6d24-4de8-902c-b74e42c74fd3	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > AURORAE	1
6141	207	ELECTRIC FIELDS/ELECTRIC CURRENTS	9abe9fdb-59f3-4bd6-b24f-b9b7e46eae7c	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > ELECTRIC FIELDS/ELECTRIC CURRENTS	1
6142	207	GEOMAGNETIC FORECASTS	882d9a10-713c-4b58-8c7b-d9af086115a3	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > GEOMAGNETIC FORECASTS	1
6143	207	GEOMAGNETIC INDICES	990016e0-f247-4c36-8a17-f50e792a964a	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > GEOMAGNETIC INDICES	1
6144	207	ION CHEMISTRY/IONIZATION	ba75172a-6965-40cf-bf3f-6c0af2f97dad	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > ION CHEMISTRY/IONIZATION	1
6189	211	ICE SHEETS	b2800856-f1e3-41aa-bdc4-75e9cd626d3f	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > ICE SHEETS	1
6145	207	MAGNETIC FIELDS/MAGNETIC CURRENTS	8cbdfa00-852c-452d-8013-86145ad318c8	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > MAGNETIC FIELDS/MAGNETIC CURRENTS	1
6146	207	MAGNETIC STORMS	e453077b-b6f3-44f0-9f3d-4408bf9a69e5	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > MAGNETIC STORMS	1
6147	207	PLASMA WAVES	5f8a9188-d588-4782-a34b-07fa68380c41	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > PLASMA WAVES	1
6148	207	SOLAR WIND	5d290bd8-049b-4002-86c8-8acba563d0e1	EARTH SCIENCE > SUN-EARTH INTERACTIONS > IONOSPHERE/MAGNETOSPHERE DYNAMICS > SOLAR WIND	1
6149	208	CORONA HOLES	6a5a2ccf-3ba6-4519-bc9b-7617ef3b9087	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > CORONA HOLES	1
6150	208	CORONAL MASS EJECTIONS	6d486f25-7477-4da9-96ae-0091596ed4d2	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > CORONAL MASS EJECTIONS	1
6151	208	CORONA	1ef327e1-6139-49ff-87c3-f959ea75a511	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > CORONA	1
6152	208	COSMIC RAYS	e06822d8-b640-4d75-ac37-33ab3cc5e765	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > COSMIC RAYS	1
6153	208	SOLAR ACTIVE REGIONS	0d32a340-ee64-4795-9254-09dcaf55bf4c	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR ACTIVE REGIONS	1
6154	208	SOLAR FLARES	fa9f54b2-a101-4faf-b1dc-b6dff141c08c	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR FLARES	1
6155	208	SOLAR IMAGERY	e2fc7768-955b-4e76-935e-d33805fcc914	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR IMAGERY	1
6156	208	SOLAR IRRADIANCE	33f0ec3e-cd6d-498c-9468-749741fc12e2	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR IRRADIANCE	1
6157	208	SOLAR OSCILLATIONS	88bd8ce6-334d-4a42-8d51-5ed074ef5a89	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR OSCILLATIONS	1
6158	208	SOLAR PROMINENCES/SOLAR FILAMENTS	7b52f7f5-4102-4829-8ea3-c0dcdd36bdca	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR PROMINENCES/SOLAR FILAMENTS	1
6159	208	SOLAR RADIO WAVE EMISSIONS	25aa0f7b-89a5-46d7-b3d3-622b60032661	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR RADIO WAVE EMISSIONS	1
6160	208	SOLAR SYNOPTIC MAPS	ace2d2e5-0b9a-472e-b27b-c687b9108076	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR SYNOPTIC MAPS	1
6161	208	SOLAR ULTRAVIOLET EMISSIONS	a4390c3d-cffa-43ee-8e91-49c6d49ac371	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR ULTRAVIOLET EMISSIONS	1
6162	208	SOLAR VELOCITY FIELDS	e4fcb001-f517-4295-89dd-73292e0bf3ee	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR VELOCITY FIELDS	1
6163	208	SOLAR X-RAY EMISSIONS	a15e514b-4b44-4587-a857-34ab7e2d357e	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SOLAR X-RAY EMISSIONS	1
6164	208	SUNSPOTS	429d42ef-9b58-4068-b389-0a9e60e55486	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ACTIVITY > SUNSPOTS	1
6165	209	ALPHA PARTICLE FLUX	2217b742-b21a-4230-ba34-1af30132135d	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > ALPHA PARTICLE FLUX	1
6166	209	ELECTRON FLUX	5223ebeb-a22d-4bb9-b2b2-ed949a10ac29	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > ELECTRON FLUX	1
6167	209	HEAVY NUCLEI FLUX	67773da0-f5f1-4047-871a-1fb5a5c1621a	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > HEAVY NUCLEI FLUX	1
6168	209	ION FLUX	d9ce8e7e-44ff-4555-a910-86b87daca0c2	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > ION FLUX	1
6169	209	NEUTRAL PARTICLE FLUX	8f801f54-9ca9-4ba6-be35-fd87968f24e7	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > NEUTRAL PARTICLE FLUX	1
6170	209	PROTON FLUX	a2443978-118d-4f7c-843d-dcd0059fe949	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > PROTON FLUX	1
6171	209	SUB-ATOMIC PARTICLE FLUX	0168947c-5f28-46d8-b643-cb31af02a6de	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > SUB-ATOMIC PARTICLE FLUX	1
6172	209	X-RAY FLUX	8686285f-9949-4a22-ad80-a1bf4d43e122	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE FLUX > X-RAY FLUX	1
6173	210	ENERGY DEPOSITION	36bab763-b5d7-450a-8328-1c1f935184f4	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > ENERGY DEPOSITION	1
6174	210	PARTICLE COMPOSITION	bc02662f-d4a1-43c6-833f-836107ae6737	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > PARTICLE COMPOSITION	1
6175	210	PARTICLE DENSITY	fd42b8e3-b76c-4888-aeb7-e6486beb4b69	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > PARTICLE DENSITY	1
6176	210	PARTICLE DISTRIBUTION FUNCTIONS	c39210ba-7659-424b-a2f0-5777a1519115	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > PARTICLE DISTRIBUTION FUNCTIONS	1
6177	210	PARTICLE SPEED	68f1ff0e-2e23-4025-ba71-7f6177352311	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > PARTICLE SPEED	1
6178	210	PARTICLE TEMPERATURE	630c1f3f-73b9-4f80-bc47-4cbf1fa43788	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > PARTICLE TEMPERATURE	1
6179	210	TOTAL ELECTRON CONTENT	0b2ca4d1-a225-4243-90eb-1b482fb094a5	EARTH SCIENCE > SUN-EARTH INTERACTIONS > SOLAR ENERGETIC PARTICLE PROPERTIES > TOTAL ELECTRON CONTENT	1
6180	211	ABLATION ZONES/ACCUMULATION ZONES	a994a6f6-cfcd-45d2-95a4-0f8455a9454d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > ABLATION ZONES/ACCUMULATION ZONES	1
6181	211	FIRN	ff79c018-8d61-4811-91bc-c4ddea29677c	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > FIRN	1
6182	211	GLACIER ELEVATION/ICE SHEET ELEVATION	4d1cc756-c12a-472a-9eae-de96e0a7ba74	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER ELEVATION/ICE SHEET ELEVATION	1
6183	211	GLACIER FACIES	7b657679-78bf-4580-987d-0d1b98dcd0d2	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER FACIES	1
6184	211	GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	5ac9ae0b-901a-468e-8a42-5d6f3865a584	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	1
6185	211	GLACIER MOTION/ICE SHEET MOTION	a870d769-b815-435a-b7cc-cba5e6c27bb3	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER MOTION/ICE SHEET MOTION	1
6186	211	GLACIER THICKNESS/ICE SHEET THICKNESS	87b27ecd-c10b-4d41-8c49-b84f185c5bd4	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER THICKNESS/ICE SHEET THICKNESS	1
6187	211	GLACIER TOPOGRAPHY/ICE SHEET TOPOGRAPHY	72fdd0c7-f998-47ab-aeee-2956b9015ccb	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIER TOPOGRAPHY/ICE SHEET TOPOGRAPHY	1
6188	211	GLACIERS	4a426aab-4a95-4bf4-8449-19a72a251541	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > GLACIERS	1
6190	211	ICEBERGS	f1c79b5f-fcc2-42e7-818b-7534f79081ff	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > ICEBERGS	1
6191	212	GROUND WATER FEATURES	ae94befb-d08e-4350-8ebe-c0ba7ded8320	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER FEATURES	1
6192	212	GROUND WATER PROCESSES/MEASUREMENTS	6e4b29b7-a0c9-4e8e-b778-23b50cf8efb8	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS	1
6193	212	GROUNDWATER CHEMISTRY	8435030e-8d16-409f-a812-ace5d8ffc122	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUNDWATER CHEMISTRY	1
6194	213	ALBEDO	2ddd003d-c19f-4336-9837-316cce5efe0b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ALBEDO	1
6195	213	AVALANCHE	2565d1be-7468-4969-9367-e21719c006a1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > AVALANCHE	1
6196	213	DEPTH HOAR	67648fff-9415-4a36-a1f6-ef028dd1d9b5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > DEPTH HOAR	1
6197	213	FREEZE/THAW	4453ac7c-1869-4aef-8b06-dbdc9e63e245	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > FREEZE/THAW	1
6198	213	FROST	f3743f11-06bb-4337-969a-d5616b96038f	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > FROST	1
6199	213	ICE DEPTH/THICKNESS	fa751659-7032-447c-a581-f4e9de854070	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ICE DEPTH/THICKNESS	1
6200	213	ICE EXTENT	0fcce7dc-496f-4078-96f0-2035a73563fb	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ICE EXTENT	1
6201	213	ICE GROWTH/MELT	7c23be3f-89fc-4a85-83fc-128b0837ee83	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ICE GROWTH/MELT	1
6202	213	ICE MOTION	10068260-94c0-4e58-83ac-f9c5d6bd5748	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ICE MOTION	1
6203	213	ICE VELOCITY	cee7ed2f-3ed1-44ad-b48b-513a68bb3244	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > ICE VELOCITY	1
6204	213	LAKE ICE	a99c2917-8f91-4ec8-ad4f-7ee6200ab35d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > LAKE ICE	1
6205	213	PERMAFROST	6a7eed90-327a-4609-b952-c9617445a1d1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > PERMAFROST	1
6206	213	RIVER ICE	ad8499b4-28cb-46ed-b0fe-867ed90fce05	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > RIVER ICE	1
6207	213	SNOW COVER	6a08f79f-a621-4f8c-b5d5-e1335f9cbcec	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW COVER	1
6208	213	SNOW DENSITY	fde70d8c-d64c-4784-971d-589eedfc42d1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW DENSITY	1
6209	213	SNOW DEPTH	9512b90f-f495-41bb-9600-ff25e4cfc571	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW DEPTH	1
6210	213	SNOW ENERGY BALANCE	8b99fd5b-4be4-4d4b-bdf2-ef92df294738	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW ENERGY BALANCE	1
6211	213	SNOW FACIES	1f10a307-df15-43e2-b3fa-5fe6df619f98	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW FACIES	1
6212	213	SNOW MELT	dd6de9e1-61e7-41bf-a2dc-9d2afc690bb3	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW MELT	1
6213	213	SNOW STRATIGRAPHY	c5aaee13-289b-40b7-867d-83bd72c02b2d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW STRATIGRAPHY	1
6214	213	SNOW WATER EQUIVALENT	47d8d3db-9aea-49f3-8edd-5216736a85ef	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW WATER EQUIVALENT	1
6215	213	SNOW/ICE CHEMISTRY	9a3b0d9b-4409-439f-b23d-c07590ff919e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW/ICE CHEMISTRY	1
6216	213	SNOW/ICE TEMPERATURE	1341f3e1-9279-4ae6-9a93-6a612957efd1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > SNOW/ICE TEMPERATURE	1
6217	213	WHITEOUT	06741402-492e-4cda-926b-8897b15450e7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SNOW/ICE > WHITEOUT	1
6218	214	SURFACE WATER CHEMISTRY	1baa552d-c563-43fb-b618-54651f8b07e6	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER CHEMISTRY	1
6219	214	SURFACE WATER FEATURES	959f1861-a776-41b1-ba6b-d23c71d4d1eb	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES	1
6220	214	SURFACE WATER PROCESSES/MEASUREMENTS	9d86cd70-062a-4c39-b3f3-226abebc07f7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS	1
6221	214	WATERSHED CHARACTERISTICS	c84b61fe-720a-4240-b6c8-8dcc9ae24a36	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS	1
6222	215	CONTAMINANTS	42c6d91b-afef-4638-95c5-0d130828b2e7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS	1
6223	215	GASES	7b98fcc5-4465-45c8-a647-557432276844	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > GASES	1
6224	215	ISOTOPES	4d5f7ae1-3368-468b-825b-e72c1df24508	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > ISOTOPES	1
6225	215	NUTRIENTS	1459a39c-4781-4481-8bd9-510762865efd	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS	1
6226	215	SOLIDS	fad79bec-0672-4c71-8910-174c8985a1b9	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > SOLIDS	1
6227	215	WATER CHARACTERISTICS	f7e97dc3-1181-41b5-8b90-946eb2504110	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS	1
6228	215	WATER QUALITY INDEXES	f2130ca3-3587-4312-b6d4-138456b5ea78	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER QUALITY INDEXES	1
6229	5158	ANGSTROM EXPONENT	6e7306a1-79a5-482e-b646-74b75a1eaa48	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > AEROSOL OPTICAL DEPTH/THICKNESS > ANGSTROM EXPONENT	1
6230	5162	NON-REFRACTORY AEROSOL ORGANIC MASS	a63f4fe6-51dc-4719-95e3-a09d111774c9	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > CHEMICAL COMPOSITION > NON-REFRACTORY AEROSOL ORGANIC MASS	1
6231	5162	WATER-SOLUBLE AEROSOL ORGANIC MASS	bc6f9a64-0d00-4f39-9f1c-a4c25b373897	EARTH SCIENCE > ATMOSPHERE > AEROSOLS > CHEMICAL COMPOSITION > WATER-SOLUBLE AEROSOL ORGANIC MASS	1
6232	5187	CARBON DIOXIDE	c3b81888-8a39-4b3f-8033-4c077797bcba	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > CARBON DIOXIDE	1
6233	5187	CARBON MONOXIDE	88a1b416-1589-45a4-9923-452975ec35c7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > CARBON MONOXIDE	1
6234	5187	CHLORINATED HYDROCARBONS	cdab2cca-6767-427e-b464-09fe26ec59db	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > CHLORINATED HYDROCARBONS	1
6235	5187	FORMALDEHYDE	bc05d7d2-3c96-4bb6-b759-d45e3c673b86	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > FORMALDEHYDE	1
6236	5187	HYDROGEN CYANIDE	af157837-bdbd-4a9a-b24e-6a79adfef57f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > HYDROGEN CYANIDE	1
6237	5187	HYPOCHLOROUS MONOXIDE	c6b2279c-804f-42bf-aa8a-0c81f9ecf6cd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > HYPOCHLOROUS MONOXIDE	1
6238	5187	METHANE	7c892333-f4c4-4f81-b825-d6a86e107e9f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > METHANE	1
6239	5187	METHYL CYANIDE	35721fc2-a968-487f-ad85-6307a18e4af6	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > METHYL CYANIDE	1
6240	5187	NON-METHANE HYDROCARBONS/VOLATILE ORGANIC COMPOUNDS	06d230f1-08f8-48cc-9bbd-5f2358a84d13	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > CARBON AND HYDROCARBON COMPOUNDS > NON-METHANE HYDROCARBONS/VOLATILE ORGANIC COMPOUNDS	1
6241	5189	BROMINE MONOXIDE	39c478bd-620e-455c-904d-4621965e376c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > BROMINE MONOXIDE	1
6242	5189	CARBON TETRACHLORIDE	1ecb1e7c-50fc-4951-b610-5140475d87ed	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > CARBON TETRACHLORIDE	1
6243	5189	CHLORINE DIOXIDE	a56d397b-bff5-4a14-b54c-366470e023c7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > CHLORINE DIOXIDE	1
6244	5189	CHLORINE MONOXIDE	6f96d1bd-f6ba-437a-9079-c575c4822248	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > CHLORINE MONOXIDE	1
6245	5189	CHLORINE NITRATE	a9104127-6846-4123-8ab0-b65c61a0018d	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > CHLORINE NITRATE	1
6246	5189	CHLOROFLUOROCARBONS	e78ae4ce-807a-4417-ad6e-a458c6da6638	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > CHLOROFLUOROCARBONS	1
6247	5189	HALOCARBONS	13588158-07b6-4294-a00c-fa095b6ad4fd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HALOCARBONS	1
6248	5189	HALONS	33e3c858-25ee-4a5e-a938-93779679ed06	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HALONS	1
6249	5189	HYDROCHLOROFLUOROCARBONS	f6b97280-74d0-4233-bd17-f9f3d9dd21c2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HYDROCHLOROFLUOROCARBONS	1
6250	5189	HYDROFLUOROCARBONS	ed5106fd-a73f-4203-87a3-9c9e7e85dcfc	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HYDROFLUOROCARBONS	1
6251	5189	HYDROGEN CHLORIDE	146a0a0b-1b42-41a6-b1f7-a27615b006a0	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HYDROGEN CHLORIDE	1
6252	5189	HYDROGEN FLUORIDE	ff9f8056-84d6-4fbc-abe0-9b6e82ed3f5e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HYDROGEN FLUORIDE	1
6253	5189	HYPOCHLOROUS ACID	27d63fe6-9970-46fd-9b22-a58e52efc57b	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > HYPOCHLOROUS ACID	1
6254	5189	METHANOL	228c14d1-e9bf-4c25-a67b-92c99bc2a8b7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > METHANOL	1
6255	5189	METHYL BROMIDE	9b6ca807-7719-48aa-864d-ebb45a519ff8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > METHYL BROMIDE	1
6256	5189	METHYL CHLORIDE	676248f0-75cd-466d-93f1-351440027c82	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HALOCARBONS AND HALOGENS > METHYL CHLORIDE	1
6257	5190	HYDROPEROXY	d8494f01-bcec-4232-ad78-fbd92c242e62	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HYDROGEN COMPOUNDS > HYDROPEROXY	1
6258	5190	HYDROXYL	5b49fd6d-3759-4b61-8b04-8309f38b2f90	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HYDROGEN COMPOUNDS > HYDROXYL	1
6259	5190	MOLECULAR HYDROGEN	e073c9d4-5a61-436c-8890-2695c4e825eb	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > HYDROGEN COMPOUNDS > MOLECULAR HYDROGEN	1
6260	5191	AMMONIA	6a745a5e-829c-43f5-8d5a-6fb549e7b81b	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > AMMONIA	1
6261	5191	CLOUD-SCREENED TOTAL COLUMN NITROGEN DIOXIDE (NO2)	6c5a6bbe-a12f-4030-9220-2013db36cf47	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > CLOUD-SCREENED TOTAL COLUMN NITROGEN DIOXIDE (NO2)	1
6262	5191	CLOUD-SCREENED TROPOSHERIC COLUMN NO2	d92ae6cc-989b-45b8-92d3-68008356c2b0	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > CLOUD-SCREENED TROPOSHERIC COLUMN NO2	1
6263	5191	DINITROGEN PENTOXIDE	9ca9519d-c62b-42ea-8c91-cad06cfc59cb	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > DINITROGEN PENTOXIDE	1
6264	5191	MOLECULAR NITROGEN	3c3b37d4-b934-4057-b8e4-438523ae88e3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > MOLECULAR NITROGEN	1
6265	5191	NITRIC ACID	b7bbed0f-24a1-44d8-a10d-92541cd2c05b	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > NITRIC ACID	1
6266	5191	NITRIC OXIDE	82a60ed8-5414-4ce0-858c-c50b27b12bc8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > NITRIC OXIDE	1
6267	5191	NITROGEN DIOXIDE	f8e65155-27c1-483e-a9b8-85399897c3ae	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > NITROGEN DIOXIDE	1
6268	5191	NITROGEN OXIDES	e82ebd1c-8241-4ca0-95a9-a6e1432519cd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > NITROGEN OXIDES	1
6269	5191	NITROUS OXIDE	cf08917f-4cef-456f-99b0-57dc468da877	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > NITROUS OXIDE	1
6270	5191	Peroxyacyl Nitrate	d44d3115-91d1-4655-9e6e-babfe39e1632	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > NITROGEN COMPOUNDS > Peroxyacyl Nitrate	1
6271	5192	MOLECULAR OXYGEN	61f4f3d0-7895-4cce-94e3-d249001d5ee8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > OXYGEN COMPOUNDS > MOLECULAR OXYGEN	1
6272	5192	OZONE	dd316647-9043-40c3-9329-f22f9215fefa	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > OXYGEN COMPOUNDS > OZONE	1
6273	5193	PHOTOLYSIS RATES	0fd2b083-e65c-443b-9794-2c355ebac06b	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > PHOTOCHEMISTRY > PHOTOLYSIS RATES	1
6274	5194	CARBONYL SULFIDE	bde65cfd-faec-4656-bc27-22dfe30912b7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS > CARBONYL SULFIDE	1
6275	5194	DIMETHYL SULFIDE	5d282de9-162a-4aeb-a48d-4569fbbd5205	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS > DIMETHYL SULFIDE	1
6276	5194	SULFATE	2ab4134d-1ac7-4421-a7a6-659a542aff4c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS > SULFATE	1
6277	5194	SULFUR DIOXIDE	f5717312-c3ca-4492-a166-9f17c6d9b273	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS > SULFUR DIOXIDE	1
6278	5194	SULFUR OXIDES	cc676fb2-cf17-413d-bb00-0b95d231f157	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC CHEMISTRY > SULFUR COMPOUNDS > SULFUR OXIDES	1
6320	5248	SUBLIMATION	d438f0a2-5a88-4d56-8bec-7c5e35249544	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > SUBLIMATION	1
6279	5236	SHORTWAVE DOWNWARD IRRADIANCE	e1af236f-ee88-4b10-8feb-70d9e09f90be	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC RADIATION > SOLAR IRRADIANCE > SHORTWAVE DOWNWARD IRRADIANCE	1
6280	5243	COMMON SENSE CLIMATE INDEX	1d527151-57b2-49ed-9937-c1756a704ce9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > COMMON SENSE CLIMATE INDEX	1
6281	5243	COOLING DEGREE DAYS	2590519a-c2bb-448a-b2f3-d10aaa7e057c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > COOLING DEGREE DAYS	1
6282	5243	FREEZING INDEX	2329bf96-d927-4993-95f9-93551d787ad7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > FREEZING INDEX	1
6283	5243	GROWING DEGREE DAYS	a43f9a02-769d-4343-8790-fa29a0507f44	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > GROWING DEGREE DAYS	1
6284	5243	HEAT INDEX	289ca013-0526-49e0-8b87-51513702e8f4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > HEAT INDEX	1
6285	5243	HEATING DEGREE DAYS	349b4322-26ff-4b3c-90fb-b3b1afd20755	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > HEATING DEGREE DAYS	1
6286	5243	RESIDENTIAL ENERGY DEMAND TEMPERATURE INDEX	37ae8d4e-fe97-43d3-b8ee-a597e4ebfe87	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > RESIDENTIAL ENERGY DEMAND TEMPERATURE INDEX	1
6287	5243	TEMPERATURE CONCENTRATION INDEX	1c441454-851f-48e0-abb3-053ae44c0d4e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > TEMPERATURE CONCENTRATION INDEX	1
6288	5243	THAWING INDEX	746c49af-3e36-4f0a-b488-e024314d6cfa	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > THAWING INDEX	1
6289	5243	WIND CHILL INDEX	d50d0685-f42f-4693-9458-eddb9ccf5704	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > ATMOSPHERIC TEMPERATURE INDICES > WIND CHILL INDEX	1
6290	5244	AIR TEMPERATURE	f634ab55-de40-4d0b-93bc-691bf5408ccb	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > AIR TEMPERATURE	1
6291	5244	BOUNDARY LAYER TEMPERATURE	e9c3b6ca-a534-4f3e-82de-b8b921e8f312	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > BOUNDARY LAYER TEMPERATURE	1
6292	5244	DEICED TEMPERATURE	6e923275-f9e3-4faf-8a7f-2c96f3d5a280	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > DEICED TEMPERATURE	1
6293	5244	DEW POINT TEMPERATURE	0c28d9e4-c848-4628-9c00-45a540707b59	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > DEW POINT TEMPERATURE	1
6294	5244	MAXIMUM/MINIMUM TEMPERATURE	5164162a-60eb-4c94-a0f0-2caaa3bb1754	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > MAXIMUM/MINIMUM TEMPERATURE	1
6295	5244	POTENTIAL TEMPERATURE	7a0bd777-be0d-43c8-80eb-5ac58f4832de	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > POTENTIAL TEMPERATURE	1
6296	5244	SKIN TEMPERATURE	25fcdcb7-efd2-4d2f-ba57-92bbcc7ba69a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > SKIN TEMPERATURE	1
6297	5244	STATIC TEMPERATURE	a1588b7d-7307-4543-9908-76d7877c4010	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > STATIC TEMPERATURE	1
6298	5244	TEMPERATURE ANOMALIES	7ca345d4-8e15-49ae-98a7-1c387f61ea85	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > TEMPERATURE ANOMALIES	1
6299	5244	TEMPERATURE TENDENCY	449ad1fb-8010-43c7-b994-178a049d4cff	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > TEMPERATURE TENDENCY	1
6300	5244	VIRTUAL TEMPERATURE	fd19a3f1-8eeb-49ab-bcaf-e7b4b267d415	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > VIRTUAL TEMPERATURE	1
6301	5245	BOUNDARY LAYER TEMPERATURE	7f94b0e5-edc6-4724-bd84-404896e09afe	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > BOUNDARY LAYER TEMPERATURE	1
6302	5245	DEICED TEMPERATURE	b3e6afd7-35a6-4cdb-a066-654a17168253	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > DEICED TEMPERATURE	1
6303	5245	DEW POINT TEMPERATURE	76103e17-59c2-4458-972d-9ff9801e5d32	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > DEW POINT TEMPERATURE	1
6304	5245	TEMPERATURE ANOMALIES	1e76ccc7-2729-4de1-8c01-f295476ebb35	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > TEMPERATURE ANOMALIES	1
6305	5245	VERTICAL PROFILES	72304037-ce59-451a-beeb-4258f3db296a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VERTICAL PROFILES	1
6306	5245	VIRTUAL TEMPERATURE	3afb06fa-96b7-4bf4-a6b7-b5fa626afc04	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VIRTUAL TEMPERATURE	1
6307	5246	DEW POINT TEMPERATURE	731beb11-9418-40ec-8f2c-c4b320e8231a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > DEW POINT TEMPERATURE	1
6308	5246	HUMIDITY	427e5121-a142-41cb-a8e9-a70b7f98eb6a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY	1
6309	5246	LAYERED PRECIPITABLE WATER	871f5bee-ea8d-44c0-8740-9b0153fa6ea4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > LAYERED PRECIPITABLE WATER	1
6310	5246	SATURATION VAPOR PRESSURE	1a2332d9-fd69-4002-89a5-203d748a4e21	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > SATURATION VAPOR PRESSURE	1
6311	5246	STABLE ISOTOPES	df1a03f5-1cb3-4c63-870a-5a09debdf065	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > STABLE ISOTOPES	1
6312	5246	TOTAL PRECIPITABLE WATER	c3a4eb4a-4619-43cd-b890-b567d01324ea	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > TOTAL PRECIPITABLE WATER	1
6313	5246	VAPOR PRESSURE	433ea253-243d-42e4-bc61-f85eb7a73879	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > VAPOR PRESSURE	1
6314	5246	WATER VAPOR	15029eb0-6342-4066-8ac9-c50f7dbfb392	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > WATER VAPOR	1
6315	5247	HUMIDITY INDEX	07826fba-f581-4119-803e-14f3bfc2d14c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICES > HUMIDITY INDEX	1
6316	5247	WATER VAPOR TRANSPORT INDEX	425486f4-7b04-4b77-af40-563fe6ed4167	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICES > WATER VAPOR TRANSPORT INDEX	1
6317	5248	CONDENSATION	d7fbbafe-fc73-4b63-9837-3d53d2370d9d	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > CONDENSATION	1
6318	5248	EVAPORATION	b68ab978-6db6-49ee-84e2-5f37b461a998	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > EVAPORATION	1
6319	5248	EVAPOTRANSPIRATION	26fc4850-7ba9-44d8-a156-5c623e17b72f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > EVAPOTRANSPIRATION	1
6321	5248	SUPERSATURATION	293cdec2-44b7-488c-ae04-0722f0a9e8b9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > SUPERSATURATION	1
6322	5248	WATER VAPOR CONVERGENCE	5d8b1280-62a6-48f5-a9f6-ed18023e3481	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > WATER VAPOR CONVERGENCE	1
6323	5248	WATER VAPOR DIVERGENCE	957240ee-7ad8-4c62-9fd7-364371d247d7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > WATER VAPOR DIVERGENCE	1
6324	5248	WATER VAPOR FLUX	32a88fee-dfa9-4ef8-ab6d-cbc18426da53	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > WATER VAPOR FLUX	1
6325	5248	WATER VAPOR TENDENCY	5cd8b242-ac18-4d9f-85d5-eb551792d7e9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > WATER VAPOR TENDENCY	1
6326	5249	VERTICALLY RESOLVED BACKSCATTER LIGHT	1b9a1873-c02f-4b6c-906e-5da8833354d4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROFILES > VERTICALLY RESOLVED BACKSCATTER LIGHT	1
6327	5249	WATER VAPOR CONCENTRATION PROFILES	04c30b59-88ea-4311-8353-8896d4eba83f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROFILES > WATER VAPOR CONCENTRATION PROFILES	1
6328	5249	WATER VAPOR MIXING RATIO PROFILES	9fccc013-4a58-438a-b1e4-cd625aeb8204	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROFILES > WATER VAPOR MIXING RATIO PROFILES	1
6329	5250	DUST DEVILS	72c180e6-b3f3-4f9a-8d04-23f0b10735af	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > DUST DEVILS	1
6330	5250	LAND BREEZES	31fe9edf-ec85-446f-a476-4bd24ee59ae2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > LAND BREEZES	1
6331	5250	MICROBURSTS	b73a2e6a-7a8b-443e-98f4-5a77f3a9691c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > MICROBURSTS	1
6332	5250	OROGRAPHIC WINDS	a1df1d50-dd2b-4944-bda5-0cf1127e2f49	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS	1
6333	5250	SEA BREEZES	9cb8f1a4-5d2b-40d1-a7c3-c608bbe20a0b	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > SEA BREEZES	1
6334	5251	STORM RELATIVE WINDS	185b86e2-af35-42b2-b20d-f9ca6fdab493	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > STORM RELATIVE WINDS	1
6335	5251	U/V WIND COMPONENTS	1e9bb112-5dc0-47a5-8c8a-b9cb07ece7c5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > U/V WIND COMPONENTS	1
6336	5251	WIND DIRECTION TENDENCY	c455fcc4-e27d-44bc-96c6-f7a7b31911ff	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION TENDENCY	1
6337	5251	WIND DIRECTION	e987550e-d443-48eb-93eb-0bc47a62d4b4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND DIRECTION	1
6338	5251	WIND SPEED TENDENCY	69526601-5607-46e0-954a-251249de80fe	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED TENDENCY	1
6339	5251	WIND SPEED	a92f49f3-e2ee-4ef4-b064-39311ffb95d3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > SURFACE WINDS > WIND SPEED	1
6340	5252	BOUNDARY LAYER WINDS	8bb1dca3-9793-4120-b0ea-f27a5b81f259	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > BOUNDARY LAYER WINDS	1
6341	5252	FLIGHT LEVEL WINDS	385af5fe-ad73-4e04-9d51-675599fb0576	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > FLIGHT LEVEL WINDS	1
6342	5252	STORM RELATIVE WINDS	b30a6184-0d59-41de-92f0-8876582ef045	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > STORM RELATIVE WINDS	1
6343	5252	U/V WIND COMPONENTS	baa4b68a-96f9-4ab3-9a9f-3df1ee1d8ff0	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > U/V WIND COMPONENTS	1
6344	5252	WIND DIRECTION TENDENCY	2a43bf40-7f23-4616-be1b-66940b7b7f4f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND DIRECTION TENDENCY	1
6345	5252	WIND DIRECTION	272ffe8a-2949-4b58-bb81-52cb1c879f4a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND DIRECTION	1
6346	5252	WIND SPEED TENDENCY	1fe29b31-b9ff-4a6c-b474-09bd9502b5c5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND SPEED TENDENCY	1
6347	5252	WIND SPEED	661591b3-6685-4de7-a2a4-9ce8ae505044	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > UPPER LEVEL WINDS > WIND SPEED	1
6348	5253	ADVECTION	ce546f0d-d2e1-43ed-b8e0-a9079c690c56	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > ADVECTION	1
6349	5253	CONVECTION	ebce0874-7635-4094-8ef4-968851873771	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > CONVECTION	1
6350	5253	CONVERGENCE	a2cc8e02-3207-4c40-af41-9656404bac0a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > CONVERGENCE	1
6351	5253	DIVERGENCE	5c58acfc-04ed-4cbf-8674-13c41b3e950d	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > DIVERGENCE	1
6352	5253	HORIZONTAL WIND VELOCITY/SPEED	8a12ec59-c8c8-4512-b123-16bca93771b0	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > HORIZONTAL WIND VELOCITY/SPEED	1
6353	5253	OROGRAPHIC LIFTING	84780569-bef5-41fd-901f-828418e390dd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > OROGRAPHIC LIFTING	1
6354	5253	STREAMFUNCTIONS	eaeb5cdd-365f-4368-8e20-6defe111b3b4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > STREAMFUNCTIONS	1
6355	5253	TURBULENCE	226d05da-dd0b-4314-919a-0b259ce724b5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > TURBULENCE	1
6356	5253	VERTICAL WIND VELOCITY/SPEED	841a7ac7-5981-4e93-895f-1b57c3d892a0	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > VERTICAL WIND VELOCITY/SPEED	1
6357	5253	VORTICITY	858a80ff-5aa4-4590-b2e2-e88a802a6ee4	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > VORTICITY	1
6358	5253	WIND SHEAR	05cf5b56-0f86-4819-b713-1272b97b06c5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > WIND SHEAR	1
6359	5253	WIND STRESS	ef034881-8bf4-403f-a4ee-c68771769c93	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > WIND STRESS	1
6360	5254	GOES WIND INDEX	8251fedc-3910-4f18-9594-df2fbb9bb1d9	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND INDICES > GOES WIND INDEX	1
6361	5254	QUASI-BIENNIAL OSCILLATION (QBO) ZONAL WIND INDEX	17e33fba-625b-40eb-b51d-902a89ca5747	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND INDICES > QUASI-BIENNIAL OSCILLATION (QBO) ZONAL WIND INDEX	1
6362	5255	LINE OF SIGHT WINDS	cd6f51f9-6ab4-4df4-a4d2-347e38fe80b6	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND PROFILES > LINE OF SIGHT WINDS	1
6363	5255	VELOCITY AZIMUTH DISPLAY VERTICAL WIND PROFILES	4478e3ea-ac49-4ea3-bcb8-e6b4e2190266	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND PROFILES > VELOCITY AZIMUTH DISPLAY VERTICAL WIND PROFILES	1
6364	5255	WIND DIRECTION PROFILES	5be35f50-a1ea-40c5-8e0d-579dad1b9143	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND PROFILES > WIND DIRECTION PROFILES	1
6365	5255	WIND VELOCITY/SPEED PROFILES	1c93710e-cfaa-47c1-ba97-b2deb85620ca	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND PROFILES > WIND VELOCITY/SPEED PROFILES	1
6366	5257	HEAT FLUX	49fd6f11-5682-4d27-8fc6-66bf3faadf39	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > HEAT FLUX	1
6367	5257	MOISTURE FLUX	925f563d-908a-4671-b750-23d0f3e42310	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > MOISTURE FLUX	1
6368	5257	RADIATIONAL COOLING	5bac3ef6-5e30-4f14-a5dc-8065c7fcba55	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > RADIATIONAL COOLING	1
6369	5257	RADIATIONAL DIVERGENCE	c7259da4-18dd-4196-91ff-a68087978349	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > RADIATIONAL DIVERGENCE	1
6370	5257	THETA-E ENTRAINMENT	cfa49843-2d36-4709-8969-b176432adf78	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > THETA-E ENTRAINMENT	1
6371	5257	VORTEX STREET	ba4a9964-8323-45df-a372-b4e2f3eef9e5	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > VORTEX STREET	1
6372	5257	WATER VAPOR TRANSPORT	a997c21b-ca61-4e78-8828-aa3e144976c3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > WATER VAPOR TRANSPORT	1
6373	5258	CLOUD CONDENSATION NUCLEI	ebbf8642-3da1-4401-a779-3e56550a029d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD CONDENSATION NUCLEI	1
6374	5258	CLOUD DROPLET CONCENTRATION/SIZE	47812ef8-b64b-4988-9ae4-31f3581ae9a5	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD DROPLET CONCENTRATION/SIZE	1
6375	5258	CLOUD LIQUID WATER/ICE	05ac9d3e-bc44-41fa-ace0-c41bf3ebee97	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD LIQUID WATER/ICE	1
6376	5258	CLOUD MASS FLUX	804fb334-1c74-4070-bd5f-848014a6e220	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD MASS FLUX	1
6377	5258	CLOUD OPTICAL DEPTH/THICKNESS	4bc483b1-dd64-4e97-bfd3-c0e755df6308	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD OPTICAL DEPTH/THICKNESS	1
6378	5258	CLOUD PRECIPITABLE WATER	b709d6fc-f0cf-47de-bdbb-1cd875b5f3ab	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > CLOUD PRECIPITABLE WATER	1
6379	5258	COLLISION RATE	76bcb8e0-1c07-4783-9d15-3a22203f7849	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > COLLISION RATE	1
6380	5258	DROPLET GROWTH	63effad4-4323-486d-a81b-e0bf3264e5c9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > DROPLET GROWTH	1
6381	5258	PARTICLE SIZE DISTRIBUTION	00d6fb2f-16d5-4949-afec-a1adbd600a58	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > PARTICLE SIZE DISTRIBUTION	1
6382	5258	SEDIMENTATION	8d66dbbe-886e-449d-bfd2-93fc8d357ccd	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > SEDIMENTATION	1
6383	5259	CLOUD ASYMMETRY	4c737490-1486-418f-81f4-c50c47da117d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD ASYMMETRY	1
6384	5259	CLOUD BASE HEIGHT	1f0765e3-4ea3-42be-8ed5-3e26bdebb219	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD BASE HEIGHT	1
6385	5259	CLOUD BASE PRESSURE	17f212af-e782-4196-b467-060699ecf4ca	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD BASE PRESSURE	1
6386	5259	CLOUD BASE TEMPERATURE	5f5f4f7a-ea5f-40fe-ba73-8d5f7241e5fa	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD BASE TEMPERATURE	1
6387	5259	CLOUD CEILING	88dc0be1-7427-4a82-9fee-3b2bf84d002a	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD CEILING	1
6388	5259	CLOUD FRACTION	b296b688-0ff0-4212-9b30-30e9fe413709	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD FRACTION	1
6389	5259	CLOUD FREQUENCY	acb52274-6c0d-4241-a979-3fa3efca6702	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD FREQUENCY	1
6390	5259	CLOUD HEIGHT	57292a97-19be-4fae-b2f7-9fa0a3629b53	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD HEIGHT	1
6391	5259	CLOUD MIDLAYER TEMPERATURE	2ca13dfa-c2b3-47de-8175-f0723151ef28	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD MIDLAYER TEMPERATURE	1
6392	5259	CLOUD TOP HEIGHT	0893cf38-fe6e-4ebc-95f4-db7d24c874db	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD TOP HEIGHT	1
6393	5259	CLOUD TOP PRESSURE	1a217e7e-74fa-438e-b4bd-5ad574d92e9d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD TOP PRESSURE	1
6394	5259	CLOUD TOP TEMPERATURE	4dc3fcab-a947-47b9-b9a1-acb2a23ee478	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD TOP TEMPERATURE	1
6395	5259	CLOUD VERTICAL DISTRIBUTION	f2902c27-0872-4ea4-98b9-706855bcd7a3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD PROPERTIES > CLOUD VERTICAL DISTRIBUTION	1
6396	5260	ABSORPTION	d2e93932-0231-4b23-af2f-217c6315a95e	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > ABSORPTION	1
6397	5260	CLOUD EMISSIVITY	576b5025-dc0e-4021-b8ff-6a7699a79b0c	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > CLOUD EMISSIVITY	1
6398	5260	CLOUD RADIATIVE FORCING	345ab082-59ac-4649-9a2a-a3bef0d26a06	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > CLOUD RADIATIVE FORCING	1
6399	5260	CLOUD REFLECTANCE	8a6572c3-676a-41dd-851f-836ac9f1f1d9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > CLOUD REFLECTANCE	1
6400	5260	DROPLET GROWTH	4d5273ad-febb-47f6-bdb7-ededf9f9eb1e	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > DROPLET GROWTH	1
6401	5260	EMISSION	4b12439a-45fc-42fa-ae19-535826f6247b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > EMISSION	1
6402	5260	SCATTERING	c830ad5e-ac31-41cf-b8e2-277fe457d76d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD RADIATIVE TRANSFER > SCATTERING	1
6403	5262	CLOUD CLUSTERS	4074eb32-a3de-494f-a722-2deeaab76b33	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CLOUD CLUSTERS	1
6404	5262	CUMULONIMBUS	7c4d5f8f-4809-4859-b379-3b8c379bc83c	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULONIMBUS	1
6405	5262	CUMULUS	e1dff4d5-2e5b-46e7-9804-9de29fdb36d9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS	1
6406	5262	DEEP CONVECTIVE CLOUD SYSTEMS	879cccd4-d375-40f6-8bee-6f58efd2dd61	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > DEEP CONVECTIVE CLOUD SYSTEMS	1
6407	5262	MESOSCALE CONVECTIVE COMPLEX	d13661da-d022-439a-bb27-dc2273f9dc88	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > MESOSCALE CONVECTIVE COMPLEX	1
6408	5262	PERCENT CONVECTIVE CLOUDS	c3ee0a52-266b-45e4-adad-d0675699676b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > PERCENT CONVECTIVE CLOUDS	1
6409	5262	PRECIPITATING CONVECTIVE CLOUD SYSTEMS	ca7f5dbd-199e-4cc8-bc7b-550753ecbc93	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > PRECIPITATING CONVECTIVE CLOUD SYSTEMS	1
6410	5262	SQUALL LINE	c6024258-d344-4cd2-932b-31e5c81a9c4b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > SQUALL LINE	1
6411	5262	TROPICAL OCEANIC CLOUD SYSTEMS	fe2e0b6f-3d7d-489a-b093-86ed0d233385	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > TROPICAL OCEANIC CLOUD SYSTEMS	1
6412	5263	NOCTILUCENT CLOUDS	939c0a66-0340-425b-999a-44a09046ec93	EARTH SCIENCE > ATMOSPHERE > CLOUDS > MESOSPHERIC CLOUDS (OBSERVED/ANALYZED) > NOCTILUCENT CLOUDS	1
6413	5263	POLAR MESOSPHERIC CLOUDS	0a7f50ce-4968-46c8-86a6-23ea13c1830c	EARTH SCIENCE > ATMOSPHERE > CLOUDS > MESOSPHERIC CLOUDS (OBSERVED/ANALYZED) > POLAR MESOSPHERIC CLOUDS	1
6414	5264	POLAR STRATOSPHERIC CLOUDS/NACREOUS	9d3d400c-ded2-4b3c-8d0c-5a76e25be033	EARTH SCIENCE > ATMOSPHERE > CLOUDS > STRATOSPHERIC CLOUDS (OBSERVED/ANALYZED) > POLAR STRATOSPHERIC CLOUDS/NACREOUS	1
6415	5265	CIRROCUMULUS	e59c154f-cdc9-4400-a0d2-af60df9e1b56	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CIRROCUMULUS	1
6416	5265	CIRROSTRATUS	bf271f69-3294-44d6-bfa8-a8f54468ca30	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CIRROSTRATUS	1
6417	5265	CIRRUS/SYSTEMS	8ce319a5-9b49-49e3-8981-3ce512c7efb0	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CIRRUS/SYSTEMS	1
6418	5265	CONTRAILS	cf75769c-2430-4280-b9c2-ba384849a548	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CONTRAILS	1
6419	5265	PILEUS	31c8b1d1-1e46-4c40-a23f-0db327121eb7	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > PILEUS	1
6420	5266	FOG	94668478-3b79-4819-847e-b154bf241aa3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG	1
6421	5266	NIMBOSTRATUS	a3d37438-644d-448e-95ea-991d79b3a0f3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > NIMBOSTRATUS	1
6422	5266	STRATOCUMULUS	3375096a-7782-42e8-97d2-0febf63893e0	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS	1
6423	5266	STRATUS	8945d3c7-1c39-4a8b-b954-2a84da8ecc88	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATUS	1
6424	5267	ALTOCUMULUS	01021105-60ed-479a-a35b-faa73e286264	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOCUMULUS	1
6425	5267	ALTOSTRATUS	f58d0203-0070-422c-ab52-6ca8ffbb6362	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOSTRATUS	1
6426	5269	CENTRAL INDIAN PRECIPITATION INDEX	c6e7ddb6-1f7c-4364-8fb4-aabd1f4dcab4	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ATMOSPHERIC PRECIPITATION INDICES > CENTRAL INDIAN PRECIPITATION INDEX	1
6427	5269	ENSO PRECIPITATION INDEX	284738a2-4fcb-4eee-9ee7-5eac2378f46d	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ATMOSPHERIC PRECIPITATION INDICES > ENSO PRECIPITATION INDEX	1
6428	5269	STANDARDIZED PRECIPITATION INDEX	3b024dec-76c2-4995-a9ad-7e2bf4feda72	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ATMOSPHERIC PRECIPITATION INDICES > STANDARDIZED PRECIPITATION INDEX	1
6429	5269	WEIGHTED ANOMALY STANDARDIZED PRECIPITATION INDEX	dc9c73a3-689c-44b5-b8fe-a5229168193e	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > ATMOSPHERIC PRECIPITATION INDICES > WEIGHTED ANOMALY STANDARDIZED PRECIPITATION INDEX	1
6430	5272	DRIZZLE	0ffab597-284f-4d1a-b026-a78a6604cec5	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > DRIZZLE	1
6431	5272	LIQUID SURFACE PRECIPITATION RATE	09d991ca-020a-4d20-910a-747ea683e1f8	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > LIQUID SURFACE PRECIPITATION RATE	1
6432	5272	RAIN	09a57dc7-3911-4a65-9f12-b819652b8671	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > RAIN	1
6433	5274	12 HOUR PRECIPITATION AMOUNT	feef8827-92a6-4d1d-b6a5-ecda38a32656	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT > 12 HOUR PRECIPITATION AMOUNT	1
6434	5274	24 HOUR PRECIPITATION AMOUNT	12250935-8f40-4279-aada-2f22cbef1459	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT > 24 HOUR PRECIPITATION AMOUNT	1
6435	5274	3 AND 6 HOUR PRECIPITATION AMOUNT	039bbfd2-7653-4ba8-9003-b46d367c6038	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT > 3 AND 6 HOUR PRECIPITATION AMOUNT	1
6436	5274	HOURLY PRECIPITATION AMOUNT	2f0f103a-4fe9-429f-a783-ba1d6e6a446a	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION AMOUNT > HOURLY PRECIPITATION AMOUNT	1
6437	5276	LATENT HEAT FLUX	9985d211-1056-4a7a-a1c8-550923ea5a81	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION PROFILES > LATENT HEAT FLUX	1
6438	5276	MELTING LAYER HEIGHT	ce105b93-42b1-4692-a8ef-dc10792f26bf	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION PROFILES > MELTING LAYER HEIGHT	1
6439	5276	RAIN TYPE	e3973025-f274-44f1-9ff5-0d2fd7e006c2	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > PRECIPITATION PROFILES > RAIN TYPE	1
6440	5279	CONVECTIVE SURFACE PRECIPITATION RATE	6c8581e8-d49c-423e-9b38-3be406b64efa	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > CONVECTIVE SURFACE PRECIPITATION RATE	1
6441	5279	HAIL	7118d286-6629-48e5-931f-052cd347395e	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > HAIL	1
6442	5279	ICE PELLETS	cac27b59-7810-4132-87b4-53108663584e	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > ICE PELLETS	1
6443	5279	SNOW	b51b3708-a662-4cf1-bf13-e67f36b001c4	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > SNOW	1
6444	5284	EXTRATROPICAL CYCLONE FREQUENCY	10277cb5-5a11-47a2-8578-3ac1c7152cd2	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > EXTRATROPICAL CYCLONES > EXTRATROPICAL CYCLONE FREQUENCY	1
6445	5284	EXTRATROPICAL CYCLONE MOTION	2357d9ae-3376-4c4e-8533-6193bf177345	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > EXTRATROPICAL CYCLONES > EXTRATROPICAL CYCLONE MOTION	1
6446	5284	EXTRATROPICAL CYCLONE TRACK	7de1c2c0-89c2-4841-b0b8-158224c8ad22	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > EXTRATROPICAL CYCLONES > EXTRATROPICAL CYCLONE TRACK	1
6447	5286	FIRST FREEZE/FROST DATE	2cc64007-a443-45d8-bf9d-c9fae69f4554	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > FIRST FREEZE/FROST DATE	1
6448	5286	FIRST FREEZE/FROST PROBABILITY	53b7e7d6-2aeb-4636-bae1-c7cd92d3d541	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > FIRST FREEZE/FROST PROBABILITY	1
6449	5286	FIRST MODERATE FREEZE/FROST DATE	581d6ad6-2132-45cf-b6be-72341024587b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > FIRST MODERATE FREEZE/FROST DATE	1
6450	5286	FREEZE FREE PERIOD LENGTH	5a0347ba-2684-4c4a-adc0-ddb63cbbde6b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > FREEZE FREE PERIOD LENGTH	1
6451	5286	LAST FREEZE/FROST DATE	fc768468-62d4-40fa-8880-a773a855a496	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > LAST FREEZE/FROST DATE	1
6452	5286	LAST FREEZE/FROST PROBABILITY	22b3623a-66c6-4616-8a6a-139ce119f672	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > LAST FREEZE/FROST PROBABILITY	1
6453	5286	LAST MODERATE FREEZE/FROST DATE	a8cc5031-9c46-4a73-a999-68cdaec453a5	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > FREEZE/FROST > LAST MODERATE FREEZE/FROST DATE	1
6454	5289	TOTAL FREEZING RAIN ACCUMULATION	0df15471-3175-44c0-aa8b-5178dfeb27a0	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > ICE STORMS > TOTAL FREEZING RAIN ACCUMULATION	1
6455	5293	BLIZZARDS	3d4f9f5a-912b-4dc1-b1c5-cd0fd9bbd3d3	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SNOW STORMS > BLIZZARDS	1
6456	5293	LAKE EFFECT SNOW	12b7f57f-c295-4adf-97f5-43356f1270bf	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SNOW STORMS > LAKE EFFECT SNOW	1
6457	5294	SUBTROPICAL DEPRESSION	99ad9306-0a99-402a-961f-acb9255cb113	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES > SUBTROPICAL DEPRESSION	1
6458	5294	SUBTROPICAL STORM	ca133c4d-9751-4b92-a1ec-013ef625ad7b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES > SUBTROPICAL STORM	1
6459	5295	CONVECTIVE AVAILABLE POTENTIAL ENERGY (CAPE)	00748b19-30cc-4d12-a7a3-0aa8b3be5a94	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices > CONVECTIVE AVAILABLE POTENTIAL ENERGY (CAPE)	1
6460	5295	K-index (KI)	1d8a8e42-0fc0-4ce1-a058-9fa961c9d4ac	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices > K-index (KI)	1
6461	5295	LIFTED INDEX (LI)	f07365c3-a36e-4a28-8364-be3941fae000	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices > LIFTED INDEX (LI)	1
6462	5295	SHOWALTER STABILITY INDEX (SI)	bd0c62a2-5336-4b41-81e1-089ce118651a	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices > SHOWALTER STABILITY INDEX (SI)	1
6463	5295	TOTAL TOTALS INDEX (TT)	77bcf3f2-8d61-4b18-9e2a-439310197c83	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > Stability/Severe Weather Indices > TOTAL TOTALS INDEX (TT)	1
6464	5296	DESTRUCTION POTENTIAL INDEX	8fd6e7bc-df59-4637-b1e7-d6715fb3e8af	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > DESTRUCTION POTENTIAL INDEX	1
6465	5296	ENHANCED FUJITA SCALE RATING	d866f0ba-c70a-4377-9f91-58ab402f6f8b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > ENHANCED FUJITA SCALE RATING	1
6466	5296	STORM SYSTEM MOTION	d9969cf1-6a1f-4f37-91bf-c746aeba81c4	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > STORM SYSTEM MOTION	1
6467	5296	TORNADO CLIMATOLOGY	d912e61f-6c95-449d-9bee-2eac2f599b8f	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO CLIMATOLOGY	1
6468	5296	TORNADO DENSITY	9a310897-86d4-4a31-9fe3-4b4ad45b3575	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO DENSITY	1
6469	5296	TORNADO FREQUENCY	de691f09-0ef3-4795-bac0-1ed15c3e7f8b	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO FREQUENCY	1
6470	5296	TORNADO PATH LENGTH	b253d76b-d48a-4d7a-abbe-7d02f783176e	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO PATH LENGTH	1
6471	5296	TORNADO PATH WIDTH	069ff99d-1455-4285-83d9-4f57fb0cb635	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO PATH WIDTH	1
6472	5296	TORNADO VORTEX SIGNATURE	c3354d3b-44a4-4b1a-b1dd-1243bd1640be	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > TORNADO VORTEX SIGNATURE	1
6473	5296	WATER SPOUT	2992d7d3-5ae6-4844-b0fa-4ad348e3a8c2	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TORNADOES > WATER SPOUT	1
6474	5297	ACCUMULATED CYCLONE ENERGY	2ead8ea2-0357-4c95-9483-da8149855fd4	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY	1
6475	5297	LANDFALL INTENSITY	923ab959-48ee-4db1-827a-3d672099e273	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY	1
6476	5297	MAXIMUM 1-MINUTE SUSTAINED WIND	ba286b68-a400-4c29-bd24-b8ca99967968	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND	1
6477	5297	MAXIMUM SURFACE WIND	106461af-377c-4dc0-bbd7-9769eba05321	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND	1
6478	5297	MAXIMUM WIND GUST	4b0e986f-5dce-48ca-8bad-794c97482553	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST	1
6479	5297	MINIMUM CENTRAL PRESSURE	38cefcb2-f5d6-4917-a87b-7cfba482e30d	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE	1
6480	5297	PEAK INTENSITY	c17617a1-5d2b-426f-bfe0-d8c4d4b5cfad	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY	1
6481	5297	SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 1)	27847732-2a5a-4094-9ba5-3c56ae897f87	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 1)	1
6482	5297	SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 2)	e282c375-ed1a-465b-b960-aa49118307ea	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 2)	1
6483	5297	SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 3)	530dfe77-5740-49e8-b994-9a6f82cf4adb	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 3)	1
6484	5297	SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 4)	e691d1ab-6d20-4ad6-bea6-46587e94c4ff	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 4)	1
6485	5297	SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 5)	978dd843-3a96-4d52-a7d6-31642503c267	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 5)	1
6486	5297	TROPICAL CYCLONE FORCE WIND EXTENT	eec57358-8166-443e-b595-cb831911cd42	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT	1
6487	5301	MYRIAPODS	9b5474eb-2dc8-4a8e-90b4-872f9fda80d9	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > MYRIAPODS	1
6488	5297	TROPICAL CYCLONE MOTION	cda34c9c-e59a-4dfb-9d2d-b8317e4b7f27	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION	1
6489	5297	TROPICAL CYCLONE RADIUS	104ed5fa-f65a-442e-992c-88a4fe74a66c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS	1
6490	5297	TROPICAL CYCLONE TRACK	10a9bb22-9119-4409-84c1-7c97ef31b1a1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK	1
6491	5297	TROPICAL DEPRESSION FREQUENCY	74aac882-80ae-4ecd-9585-c541cd7a10fc	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL DEPRESSION FREQUENCY	1
6492	5297	TROPICAL DEPRESSION MOTION	03e9cfd2-631c-42e6-b25c-b75f57e4ebb8	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL DEPRESSION MOTION	1
6493	5297	TROPICAL DEPRESSION TRACK	75c369df-2b9f-4328-8b1f-325d83ffb4cf	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL DEPRESSION TRACK	1
6494	5297	TROPICAL STORM FORCE WIND EXTENT	23c94a4c-db57-4d57-b24f-4dba24aa3cc6	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL STORM FORCE WIND EXTENT	1
6495	5297	TROPICAL STORM FREQUENCY	de9ffa22-76e3-469c-926b-2dee007702d0	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL STORM FREQUENCY	1
6496	5297	TROPICAL STORM MOTION	ce15b57a-9b1b-4bb7-805e-b13defd9a851	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL STORM MOTION	1
6497	5297	TROPICAL STORM TRACK	2a4bc557-ee60-4446-920a-25632f5b8b4d	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL STORM TRACK	1
6498	5298	DERECHO	4e845edf-3635-4665-9d9d-d7186c151cda	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > WIND STORMS > DERECHO	1
6499	5298	GALE	530ca9b8-50f3-4bd6-82d4-c49fa688a977	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > WIND STORMS > GALE	1
6500	5298	MICROBURST	9da19ae9-799f-4885-8fb8-564ca803639a	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > WIND STORMS > MICROBURST	1
6501	5298	SQUALL	27275638-546e-4181-b15c-ddc3524de3d5	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > WIND STORMS > SQUALL	1
6502	5301	CHELICERATES	b32ca9df-f981-4696-bf97-c190175e47b7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CHELICERATES	1
6503	5301	CRUSTACEANS	f2044dcf-40da-4fcc-97ab-914343d885a5	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS	1
6504	5301	HEXAPODS	38e40180-1a2a-40a9-a030-04775dabbabb	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > HEXAPODS	1
6505	5304	ANTHOZOANS/HEXACORALS	ad557b31-fc70-4519-a8e4-3a5daf05f774	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/HEXACORALS	1
6506	5304	ANTHOZOANS/OCTOCORALS	cbdf4f94-efc6-4965-a329-5df989a9a211	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/OCTOCORALS	1
6507	5304	HYDROZOANS	c2c891c2-aa15-40b8-bfae-f02f42d0c739	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > HYDROZOANS	1
6508	5304	JELLYFISHES	cb628a66-a10b-4ef1-9261-7ce63a9439dc	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > JELLYFISHES	1
6509	5306	BRITTLE/BASKET STARS	4c653917-a5d8-4572-a509-572e9fd2c63d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ECHINODERMS > BRITTLE/BASKET STARS	1
6510	5306	SEA STARS	ec994afa-ecd4-4d25-9e8b-335cd982755c	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ECHINODERMS > SEA STARS	1
6511	5306	SEA URCHINS	6972b6bd-2f7e-460d-b12a-914b7d1e029c	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ECHINODERMS > SEA URCHINS	1
6512	5313	APLACOPHORANS	2b24db47-ecf4-4559-aaff-aef150188b03	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > APLACOPHORANS	1
6513	5313	BIVALVES	7da8400b-e2cf-4ab1-b2f0-5bc4b21c23b3	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > BIVALVES	1
6514	5313	CEPHALOPODS	955fae6f-6aae-460a-a952-1c0c30f5151e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > CEPHALOPODS	1
6515	5313	CHITONS	e65cfeec-0da2-40d8-b80d-1c74d1a498fc	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > CHITONS	1
6516	5313	GASTROPODS	d2db293d-2ed7-4831-9794-a2cf903e4d4d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > GASTROPODS	1
6517	5320	BRISTLE WORMS	ea2c5c8f-6b57-4fcc-8c01-53343c706cef	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SEGMENTED WORMS (ANNELIDS) > BRISTLE WORMS	1
6518	5320	EARTHWORMS	517e2978-223e-42a2-b889-9c60f7099859	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SEGMENTED WORMS (ANNELIDS) > EARTHWORMS	1
6519	5320	LEECHES	b845369b-bf6b-47a6-b56a-a11438604a39	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > SEGMENTED WORMS (ANNELIDS) > LEECHES	1
6520	5323	LARVACEANS	8b1af14c-25f1-42bb-bba9-24ee5cee4e43	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > TUNICATES > LARVACEANS	1
6521	5323	SALPS	b63e1a64-661a-4228-8453-248076f612b7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > TUNICATES > SALPS	1
6522	5323	SEA SQUIRTS	9987f02e-2f2f-48ed-95ac-02514f02d7b0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > TUNICATES > SEA SQUIRTS	1
6523	5326	FROGS/TOADS	db49ac33-d70a-488c-a1f2-9aa3706ba707	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > AMPHIBIANS > FROGS/TOADS	1
6524	5326	SALAMANDERS	1ac84a15-6f6b-48e0-b7ba-796813e5ff2c	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > AMPHIBIANS > SALAMANDERS	1
6525	5327	ALBATROSSES/PETRELS AND ALLIES	b4e28ec2-c2a0-4eb4-9544-8eb227903d47	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > ALBATROSSES/PETRELS AND ALLIES	1
6526	5327	CRANES AND ALLIES	39e33722-56b0-4928-a032-d4832f7136cc	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > CRANES AND ALLIES	1
6527	5327	DUCKS/GEESE/SWANS	c310aa65-810b-4e36-9689-d37b1154fa1b	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > DUCKS/GEESE/SWANS	1
6528	5327	EAGLES/FALCONS/HAWKS AND ALLIES	3f51c987-e49b-4988-a05c-d2d9da82dd22	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > EAGLES/FALCONS/HAWKS AND ALLIES	1
6529	5327	GREBES	050ce2a5-f895-4600-a0a1-eb0e3adb09e1	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > GREBES	1
6530	5327	HERONS/EGRETS AND ALLIES	af67dee1-7c50-4e73-8db8-b1f421df67fb	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > HERONS/EGRETS AND ALLIES	1
6531	5327	IBISES/SPOONBILLS	70464ef6-7702-4b8d-bacc-50f44b0d6100	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > IBISES/SPOONBILLS	1
6532	5327	LOONS	4342be4c-fd26-4c02-b09f-e35ea4f34575	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > LOONS	1
6533	5327	PELICANS AND ALLIES	3a591a70-def2-4625-bf26-1151724dbcb4	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > PELICANS AND ALLIES	1
6534	5327	PENGUINS	a463163e-8e86-4086-8b10-8fd6a95fca4a	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > PENGUINS	1
6535	5327	PERCHING BIRDS	c8186508-c5dd-4282-86d2-b217643a87d8	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > PERCHING BIRDS	1
6536	5327	SANDPIPERS	519a7291-55a2-44a4-8f01-ca7742ff69cc	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > SANDPIPERS	1
6537	5327	WADERS/GULLS/AUKS AND ALLIES	e8f25820-dd06-4d8d-9548-dcc30a871982	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > BIRDS > WADERS/GULLS/AUKS AND ALLIES	1
6538	5328	LAMPREYS/HAGFISHES	e5404ad9-95bf-4851-9dbb-fecf7dc1e905	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > LAMPREYS/HAGFISHES	1
6539	5328	RAY-FINNED FISHES	c69cde73-7bd9-489b-a20b-bd23cfb82d92	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES	1
6540	5328	SHARKS/RAYS/CHIMAERAS	ed019e00-9b0a-4bdc-89aa-606cc929bd9f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > SHARKS/RAYS/CHIMAERAS	1
6541	5329	BATS	9db9cb8c-7d18-4922-990c-b610d22356eb	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > BATS	1
6542	5329	CARNIVORES	7a00c50c-827c-4012-9afe-20972e6a00c6	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES	1
6543	5329	CETACEANS	7f066677-c0f8-4bb1-91de-13954494a927	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CETACEANS	1
6544	5329	DUGONGS/MANATEES	af5fb4da-260e-4e4e-a332-36dfd5084e5d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > DUGONGS/MANATEES	1
6545	5329	ELEPHANTS	de9598de-24cc-4f87-b3df-d9f3d4717d33	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > ELEPHANTS	1
6546	5329	EVEN-TOED UNGULATES	7b0bc104-eed1-4bc1-b12b-3cf9add700da	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > EVEN-TOED UNGULATES	1
6547	5329	RODENTS	fae29067-5d65-455a-a515-b1ac52881285	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > RODENTS	1
6548	5330	ALLIGATORS/CROCODILES	3f1803fa-3ada-4762-96e4-28966dfdcc83	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > REPTILES > ALLIGATORS/CROCODILES	1
6549	5330	LIZARDS/SNAKES	7dce336b-8596-45f0-bc76-f82b26e1405f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > REPTILES > LIZARDS/SNAKES	1
6550	5330	TURTLES	2037d286-6285-49df-aeb4-6e429b18d595	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > REPTILES > TURTLES	1
6551	5336	DICOTS	f4211da2-9eaa-4bb3-86b1-c4595e9f2971	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > ANGIOSPERMS (FLOWERING PLANTS) > DICOTS	1
6552	5336	MONOCOTS	b2957a8b-4c60-42aa-ac1c-56a88421702b	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > ANGIOSPERMS (FLOWERING PLANTS) > MONOCOTS	1
6553	5337	CLUB MOSSES	c5ae3a71-d144-4b91-9cf0-e3cb27ce718f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > FERNS AND ALLIES > CLUB MOSSES	1
6554	5337	FERNS	9818a5f0-bec9-47c0-b2ee-7e84c55466ed	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > FERNS AND ALLIES > FERNS	1
6555	5337	HORSETAILS	5f5bbb69-57ea-4d8e-bd89-20478bc765d1	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > FERNS AND ALLIES > HORSETAILS	1
6556	5337	WHISK FERNS	e76b3409-8be4-422b-8002-85bbfa846994	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > FERNS AND ALLIES > WHISK FERNS	1
6557	5338	CONIFERS	b26769a1-f023-4ab1-bc21-78ef2a5fd185	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > GYMNOSPERMS > CONIFERS	1
6558	5338	CYCADS	2e7a8b01-ee3b-44e2-95ef-cf4603b05204	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > GYMNOSPERMS > CYCADS	1
6559	5338	GINKGO	fdccf097-a2e1-4494-ad47-1c96a4d0d99a	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > GYMNOSPERMS > GINKGO	1
6560	5338	GNETOPS	f0077bce-436c-432c-8d28-eb8d9cf2849b	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > GYMNOSPERMS > GNETOPS	1
6561	5339	BROWN ALGAE	36e07e20-ce85-4418-83fd-6d718e55f370	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MACROALGAE (SEAWEEDS) > BROWN ALGAE	1
6562	5339	GREEN ALGAE	4fb63f34-f934-4a20-9d6e-ee57424f2391	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MACROALGAE (SEAWEEDS) > GREEN ALGAE	1
6563	5339	RED ALGAE	63015ca3-455b-4d91-b047-ff83a95d6bbe	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MACROALGAE (SEAWEEDS) > RED ALGAE	1
6564	5340	CRYPTOMONADS	502c9a41-ab95-4ae7-8e92-d1024b094f36	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE > CRYPTOMONADS	1
6565	5340	DIATOMS	a14cfe48-9554-4e7c-9a2b-bf72834eafba	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE > DIATOMS	1
6566	5340	DINOFLAGELLATES	b29cf79c-92a9-4160-aa8a-6917da79e298	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE > DINOFLAGELLATES	1
6567	5340	HAPTOPHYTES	0a454dc9-de56-4682-8688-36ffd547d42f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE > HAPTOPHYTES	1
6568	5342	AMOEBAS	949f8a84-185a-42a0-89dc-48534b46f309	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > AMOEBOIDS > AMOEBAS	1
6569	5342	FORAMINIFERS	d9750f06-3784-4058-941f-40289c8d9d8b	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > AMOEBOIDS > FORAMINIFERS	1
6570	5342	RADIOLARIANS	9becd489-f8fb-4dbb-b920-6c8399100515	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > AMOEBOIDS > RADIOLARIANS	1
6571	5345	CRYPTOMONADS	802614f5-e178-4e5d-be64-a7e09ea736cb	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > FLAGELLATES > CRYPTOMONADS	1
6572	5345	DINOFLAGELLATES	a0176a92-3eff-4278-b8db-02148c990302	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > FLAGELLATES > DINOFLAGELLATES	1
6573	5345	HAPTOPHYTES	dc7d2770-86a3-463c-a92b-c61516ffb32a	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > FLAGELLATES > HAPTOPHYTES	1
6574	5346	BROWN ALGAE	e2d18940-adf6-4bdd-ab4f-fe86e68278f4	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > MACROALGAE (SEAWEEDS) > BROWN ALGAE	1
6575	5346	GREEN ALGAE	76557903-2ed7-4f0e-b8fc-df02798d724e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > MACROALGAE (SEAWEEDS) > GREEN ALGAE	1
6576	5346	RED ALGAE	b9e718df-0a3a-46b6-a34f-4960e9449660	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > MACROALGAE (SEAWEEDS) > RED ALGAE	1
6577	5347	PHYTOPLANKTON	28dc7895-3365-4bab-9946-3b247f4137b0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > PLANKTON > PHYTOPLANKTON	1
6578	5350	BIODIVERSITY FUNCTIONS	4e366444-01ea-4517-9d93-56f55ddf41b7	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > BIODIVERSITY FUNCTIONS	1
6579	5350	COMMUNITY STRUCTURE	f42c849c-7113-4c69-a01e-52ebc5e7b44d	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > COMMUNITY STRUCTURE	1
6580	5350	GRAZING DYNAMICS/PLANT ECOLOGY	c09be13f-5dc2-4460-9055-1a7232aa41ae	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > GRAZING DYNAMICS/PLANT ECOLOGY	1
6581	5350	INDICATOR SPECIES	d3c5e3e3-97bf-4e74-9f8d-523dce5f9270	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > INDICATOR SPECIES	1
6582	5350	INVASIVE SPECIES	7bfdbe8d-3945-4678-a90b-d2251f973955	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > INVASIVE SPECIES	1
6583	5350	PLANT SUCCESSION	ad7abcce-b88e-46c7-be44-496d60c88f25	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > PLANT SUCCESSION	1
6584	5350	SPECIES DOMINANCE INDICES	1a2a8cf8-6d7d-4ad6-b40c-4d9f7fed493f	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > SPECIES DOMINANCE INDICES	1
6585	5350	SPECIES RECRUITMENT	b98b8823-3e95-4383-bbb0-414ee8832112	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > COMMUNITY DYNAMICS > SPECIES RECRUITMENT	1
6586	5351	BIOGEOCHEMICAL CYCLES	9015e65f-bbae-4855-a4b6-1bfa601752bd	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > BIOGEOCHEMICAL CYCLES	1
6587	5351	BIOMASS DYNAMICS	a0eb9268-0333-4442-9bc6-efbe338d9836	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > BIOMASS DYNAMICS	1
6588	5351	CHEMOSYNTHESIS	7f8a1613-67b0-4d6a-a9ad-89097c27a052	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > CHEMOSYNTHESIS	1
6589	5351	CONSUMPTION RATES	d6464d91-2373-456f-85a7-a5019bdb1076	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > CONSUMPTION RATES	1
6590	5351	DECOMPOSITION	560eac7e-d172-4a31-a659-a3e99d5f61ac	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > DECOMPOSITION	1
6591	5351	EXCRETION RATES	16e5beb3-e3ae-49a4-8fac-302fbbcdd39c	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > EXCRETION RATES	1
6592	5351	FOOD-WEB DYNAMICS	4a55497b-8e07-431a-9af9-fece001f1dd7	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > FOOD-WEB DYNAMICS	1
6593	5351	NUTRIENT CYCLING	7a33a978-8ef6-4313-b489-c06cfc6d9cec	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > NUTRIENT CYCLING	1
6594	5351	OXYGEN DEMAND	5fb90409-f9b5-46bc-8a6a-7c42e250c7c3	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > OXYGEN DEMAND	1
6595	5351	PHOTOSYNTHESIS	07b53dde-6fea-4662-9d03-ccfd617ca710	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > PHOTOSYNTHESIS	1
6596	5351	PRIMARY PRODUCTION	ecd03762-df34-49b7-91f2-d8a51acd270e	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > PRIMARY PRODUCTION	1
6597	5351	RESPIRATION RATE	29a64468-46a8-4dbc-955d-80b7b4cf9aaf	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > RESPIRATION RATE	1
6598	5351	SECONDARY PRODUCTION	200e9b2d-0201-4f52-9a5e-6dc6c4668ec9	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > SECONDARY PRODUCTION	1
6599	5351	TROPHIC DYNAMICS	bd46a0bf-5c06-48af-a6c9-022417b1fffd	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOSYSTEM FUNCTIONS > TROPHIC DYNAMICS	1
6600	5352	BIOAVAILABILITY	8e89d525-161c-4e02-8ef8-4868e0cf8c57	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOTOXICOLOGY > BIOAVAILABILITY	1
6601	5352	SPECIES BIOACCUMULATION	a54dbc4f-c136-4648-9797-db00e62fe22b	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOTOXICOLOGY > SPECIES BIOACCUMULATION	1
6602	5352	TOXICITY LEVELS	5518feb6-93a8-46fd-9e9a-25be3a832d6d	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > ECOTOXICOLOGY > TOXICITY LEVELS	1
6603	5353	FIRE DYNAMICS	2a0a6319-80c4-49fd-8a40-553175aa8637	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > FIRE ECOLOGY > FIRE DYNAMICS	1
6604	5353	FIRE MODELS	2bfd42f1-0453-4c33-a21e-74df3ad64813	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > FIRE ECOLOGY > FIRE MODELS	1
6605	5353	FIRE OCCURRENCE	e6f1ee58-fb71-42dd-b071-c1637da7e51f	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > FIRE ECOLOGY > FIRE OCCURRENCE	1
6606	5354	BIOLUMINESCENCE	5efc3bc4-6403-4e33-ba23-5418fbc026b1	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > BIOLUMINESCENCE	1
6607	5354	DIURNAL MOVEMENTS	f75f9011-903e-4757-9fcf-fefac2599b59	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > DIURNAL MOVEMENTS	1
6608	5354	ENDANGERED SPECIES	f930dcf2-ddb4-4242-9079-9c8d5ceeaa35	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > ENDANGERED SPECIES	1
6609	5354	EVOLUTIONARY ADAPTATION	cf3d1728-7606-4561-a0dd-116b4dbec21f	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > EVOLUTIONARY ADAPTATION	1
6610	5354	EXOTIC SPECIES	ddeb06af-5c36-428d-801e-e9f9a60ce429	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > EXOTIC SPECIES	1
6611	5354	EXTINCTION RATE	f27f7bf4-53fd-41bb-8e7e-b771f48f3bcc	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > EXTINCTION RATE	1
6612	5354	GRAZING DYNAMICS/PLANT HERBIVORY	bcb43cdf-294e-463c-a114-a55bd54f0b48	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > GRAZING DYNAMICS/PLANT HERBIVORY	1
6613	5354	HIBERNATION	dfc20833-d79a-4976-91fd-db9f3efc7822	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > HIBERNATION	1
6614	5354	INDIGENOUS/NATIVE SPECIES	cd9f44da-b3b4-4f9c-a21f-89b59a29b235	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > INDIGENOUS/NATIVE SPECIES	1
6615	5354	MIGRATORY RATES/ROUTES	a4ed794f-d7b6-4e53-b565-3b86fe584ba3	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > MIGRATORY RATES/ROUTES	1
6616	5354	MUTATION RATES	87601d17-faca-42c2-a431-61cf67933095	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > MUTATION RATES	1
6617	5354	MUTUALISM	003466f4-9ee7-4d3b-81ff-2013add292e2	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > MUTUALISM	1
6618	5354	NATURAL SELECTION	80ae5fdc-c312-4fa1-bf7d-60346529976d	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > NATURAL SELECTION	1
6619	5354	PARASITISM	51f3e55c-b694-4028-86fe-604a52dc794f	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > PARASITISM	1
6620	5354	POLLINATOR SPECIES	45950ee6-adc2-4f39-96a7-c00bacd1ba9e	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > POLLINATOR SPECIES	1
6621	5354	POPULATION DYNAMICS	ad3a5f4f-4624-4a08-b875-6723c2615e90	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > POPULATION DYNAMICS	1
6622	5354	POST-BREEDING PERIODS	f173021d-afc4-4a8f-8432-30c0cf832e3b	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > POST-BREEDING PERIODS	1
6623	5354	RANGE CHANGES	615e826e-a5da-4e94-b7df-ad3515c06135	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > RANGE CHANGES	1
6624	5354	SCAVENGING	abc96dce-cbae-43a4-b7c2-2ff02276b030	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SCAVENGING	1
6625	5354	SPECIES COMPETITION	60bd0b0a-2d6f-4f3c-bf42-2c081ef48b72	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SPECIES COMPETITION	1
6626	5354	SPECIES LIFE HISTORY	fd06e0a2-f689-4b33-8a85-f38bf4966808	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SPECIES LIFE HISTORY	1
6627	5354	SPECIES PREDATION	b69d76ba-ad69-4418-8e5b-ebb659604dda	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SPECIES PREDATION	1
6628	5354	SURVIVAL RATES	fa68e752-f3a7-4361-a000-47c908545e49	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SURVIVAL RATES	1
6629	5354	SYMBIOSIS	e008a809-42eb-4694-aac2-db7b6027ee77	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > SYMBIOSIS	1
6630	5354	USE/FEEDING HABITATS	744c38f8-feeb-4e01-a909-33d75fefba82	EARTH SCIENCE > BIOSPHERE > ECOLOGICAL DYNAMICS > SPECIES/POPULATION INTERACTIONS > USE/FEEDING HABITATS	1
6631	5355	AGRICULTURAL LANDS	38fb609b-2a10-4d4f-b2e8-7e51161ec974	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > AGRICULTURAL LANDS	1
6632	5355	RESOURCE DEVELOPMENT SITE	8f109871-e6ff-4cef-a5f8-5a3ad981923e	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > RESOURCE DEVELOPMENT SITE	1
6633	5355	URBAN LANDS	3e59af3d-500b-4c66-a9a1-76db5cf4a00b	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > URBAN LANDS	1
6634	5356	PLANKTON	ca8d77f2-9257-4298-9244-e81cd890f000	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > PLANKTON	1
6635	5356	WETLANDS	b72c49a1-8276-4753-8c88-894bc7bbf60d	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS	1
6636	5357	LAKE/POND	57a3a5a7-66b9-4a4a-82da-7b09d82c684a	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > LAKE/POND	1
6637	5357	RIVERS/STREAM	43d51c24-0523-4b65-919f-17618c7d72b4	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM	1
6638	5358	ABYSSAL	1c286cb7-2668-4db3-a5ac-cb8b710bebc2	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ABYSSAL	1
6639	5358	BENTHIC	09a78997-581b-4d1b-ae71-b2b3f96ef719	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > BENTHIC	1
6640	5358	COASTAL	47be68db-d10d-43e7-b150-61cfd3f06126	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL	1
6641	5358	DEMERSAL	af953f41-ab6c-4569-9762-c46ad07118da	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > DEMERSAL	1
6642	5358	ESTUARY	5a1ebca4-057d-43b9-af6a-04f57b93f8bb	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ESTUARY	1
6643	5358	PELAGIC	3d7ecc4f-e79e-40d1-8796-63059888bf5f	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > PELAGIC	1
6644	5358	REEF	367718c8-cc3b-4c94-a270-0a278afabb43	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > REEF	1
6645	5359	ALPINE/TUNDRA	76589134-8d93-4e45-8476-f04497181d14	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > ALPINE/TUNDRA	1
6646	5359	CAVE/SUBTERRANEAN	91f6a2e5-5862-46a9-ba6a-d76e06d9997c	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > CAVE/SUBTERRANEAN	1
6647	5359	DESERTS	5d5426f6-e7ce-41c1-a3d3-b93adf748f0f	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > DESERTS	1
6648	5359	FORESTS	46e4aaa4-349c-4049-a910-035391360010	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS	1
6649	5359	GRASSLANDS	142ea0c1-b77f-44da-8c64-ac7ee13fd5f6	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > GRASSLANDS	1
6650	5359	ISLANDS	fa3c6df8-a1e1-41d5-9de1-49b92e1ea455	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > ISLANDS	1
6651	5359	KARST LANDSCAPE	de702fdd-3702-4164-a396-08082b0558c0	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > KARST LANDSCAPE	1
6652	5359	MONTANE HABITATS	99e09719-f1f8-439e-be4c-759242612a84	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > MONTANE HABITATS	1
6653	5359	SAVANNAS	f8d55ee4-1efb-4d83-b07f-1029ab0fa9e1	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > SAVANNAS	1
6654	5359	SHRUBLAND/SCRUB	e018b139-7e05-4155-8e2e-8d5603b5fe47	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > SHRUBLAND/SCRUB	1
6655	5359	WETLANDS	7da95c01-4b39-437e-a8d4-fd572e43f693	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS	1
6656	5374	LEAF AREA INDEX (LAI)	f829171e-8b22-4f93-8f71-7932dfd7a70b	EARTH SCIENCE > BIOSPHERE > VEGETATION > LEAF CHARACTERISTICS > LEAF AREA INDEX (LAI)	1
6657	5380	FRACTION OF ABSORBED PHOTOSYNTHETICALLY ACTIVE RADIATION (FAPAR)	6079e5e4-4dee-4b32-aaa8-ae3231bcbadb	EARTH SCIENCE > BIOSPHERE > VEGETATION > PHOTOSYNTHETICALLY ACTIVE RADIATION > FRACTION OF ABSORBED PHOTOSYNTHETICALLY ACTIVE RADIATION (FAPAR)	1
6658	5382	VEGETATION WATER CONTENT	ff141ffe-05ea-4901-a243-e6186826b05c	EARTH SCIENCE > BIOSPHERE > VEGETATION > PLANT CHARACTERISTICS > VEGETATION WATER CONTENT	1
6659	5389	LEAF AREA INDEX (LAI)	b1d65d88-7bd0-491d-91ca-4102b89dc3e7	EARTH SCIENCE > BIOSPHERE > VEGETATION > VEGETATION INDEX > LEAF AREA INDEX (LAI)	1
6660	5389	NORMALIZED DIFFERENCE VEGETATION INDEX (NDVI)	2297a00a-80f5-466e-b28e-b9ca42562d3f	EARTH SCIENCE > BIOSPHERE > VEGETATION > VEGETATION INDEX > NORMALIZED DIFFERENCE VEGETATION INDEX (NDVI)	1
6661	5391	INCREASED/DECREASED CLOUD FRACTION	2111d240-315c-411b-8114-7ef9e89317e5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > CLOUD INDICATORS > INCREASED/DECREASED CLOUD FRACTION	1
6662	5393	EXTREME DROUGHT	e4c806af-ab57-4fda-b7e9-29e3c65f6ec5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER > EXTREME DROUGHT	1
6663	5393	EXTREME PRECIPITATION	fc5a1b7a-5ee8-4d67-80f5-a57e3f1734ab	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER > EXTREME PRECIPITATION	1
6664	5393	HEAT/COLD WAVE FREQUENCY/INTENSITY	079e6699-efbf-4358-9047-b668b459fc22	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER > HEAT/COLD WAVE FREQUENCY/INTENSITY	1
6665	5393	MONSOON ONSET/INTENSITY	7f95ceda-09fd-4ee3-9f30-bf38bf831e12	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER > MONSOON ONSET/INTENSITY	1
6666	5393	TROPICAL OR EXTRATROPICAL CYCLONE FREQUENCY/INTENSITY	a85b812e-e4d2-4dce-bf67-d89a3e1a9122	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > EXTREME WEATHER > TROPICAL OR EXTRATROPICAL CYCLONE FREQUENCY/INTENSITY	1
6667	5395	HUMIDITY INDEX	cdd7a31f-3244-494d-bc44-7b5f1ebb4bd7	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES > HUMIDITY INDEX	1
6668	5395	TEMPERATURE-HUMIDITY INDEX	5bdc74e2-ea3a-4d1d-b64e-9eaf3a879545	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES > TEMPERATURE-HUMIDITY INDEX	1
7295	6087	CRUSTAL MOTION	8dd8d272-fb6d-4eec-882a-f3be98800b42	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > CRUSTAL MOTION	1
6669	5395	WATER VAPOR TRANSPORT INDEX	b9349099-8d45-4260-ab30-c891c3553a25	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES > WATER VAPOR TRANSPORT INDEX	1
6670	5397	OCEAN COASTAL UPWELLING INDEX	74ad118c-2f18-40fb-a26e-092390f52c20	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > OCEAN UPWELLING INDICES > OCEAN COASTAL UPWELLING INDEX	1
6671	5399	PRECIPITATION TRENDS	279961c4-dac3-4188-917f-fa11982f957e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICATORS > PRECIPITATION TRENDS	1
6672	5399	PRECIPITATION VARIABILITY	c7c88080-660c-4913-8140-5f3bc91e295e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICATORS > PRECIPITATION VARIABILITY	1
6673	5399	SAHEL STANDARDIZED RAINFALL	e13b084e-d044-49c9-8791-f057f777fca3	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICATORS > SAHEL STANDARDIZED RAINFALL	1
6674	5400	ENSO PRECIPITATION INDEX	d14d762c-4117-438a-9093-a098a0d0e4e6	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICES > ENSO PRECIPITATION INDEX	1
6675	5400	NORTHEAST BRAZIL RAINFALL ANOMALY	b8f0571c-4c19-4025-936c-936e9ac72e21	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICES > NORTHEAST BRAZIL RAINFALL ANOMALY	1
6676	5400	STANDARDIZED PRECIPITATION INDEX	7427fb2d-43b5-478a-960d-2ff9aa398462	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICES > STANDARDIZED PRECIPITATION INDEX	1
6677	5400	WEIGHTED ANOMALY STANDARDIZED PRECIPITATION INDEX	aefbd3c5-6594-455b-a99d-7397a694bf8e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > PRECIPITATION INDICES > WEIGHTED ANOMALY STANDARDIZED PRECIPITATION INDEX	1
6678	5401	EROSION	eec5b471-bcc5-4d9b-8274-f3990e79ed84	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA LEVEL RISE > EROSION	1
6679	5401	INUNDATION	9db10fb2-0ceb-412e-9936-a286c579fa9f	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA LEVEL RISE > INUNDATION	1
6680	5402	ATLANTIC TRIPOLE SST	ca418285-d1f2-4348-82e4-7fc59f8b60c8	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > ATLANTIC TRIPOLE SST	1
6681	5402	CARIBBEAN INDEX	5f2273b8-be30-45d5-a5d7-9bd947779c2e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > CARIBBEAN INDEX	1
6682	5402	CENTRAL TROPICAL PACIFIC SST	ad5bde75-1f54-4f7e-a958-3adaf9f40639	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > CENTRAL TROPICAL PACIFIC SST	1
6683	5402	EAST CENTRAL TROPICAL PACIFIC SST	01b96758-13f3-4cea-8447-decae36b1bde	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > EAST CENTRAL TROPICAL PACIFIC SST	1
6684	5402	EXTREME EASTERN TROPICAL PACIFIC SST	4b862c68-9cd9-4fee-942a-7cec0e6b05c2	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > EXTREME EASTERN TROPICAL PACIFIC SST	1
6685	5402	KAPLAN SST INDEX	9c98dcbd-1dc8-4e0a-8ad1-0d11e88360eb	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > KAPLAN SST INDEX	1
6686	5402	NINO 3 INDEX	c58dc7fb-65d5-4309-8abe-160e8e845382	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > NINO 3 INDEX	1
6687	5402	NORTH TROPICAL ATLANTIC INDEX	d52674c3-0c78-4f35-9675-c2a8b3869b16	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > NORTH TROPICAL ATLANTIC INDEX	1
6688	5402	OCEANIC NINO INDEX	70ed535b-a591-411d-80ca-9eafe10b3be8	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > OCEANIC NINO INDEX	1
6689	5402	PACIFIC WARM POOL	db1000b8-3b19-46fa-9d79-379379d654ac	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > PACIFIC WARM POOL	1
6690	5402	TRANS-NINO INDEX	58d71334-7fb5-4e05-85fd-9d2485854abe	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TRANS-NINO INDEX	1
6691	5402	TROPICAL NORTH ATLANTIC INDEX	2cde80e8-3eb1-40e7-9305-e765dc8df5e2	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TROPICAL NORTH ATLANTIC INDEX	1
6692	5402	TROPICAL PACIFIC SST EOF	ed2f3a3f-c841-41cf-9394-3a3254d13fc2	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TROPICAL PACIFIC SST EOF	1
6693	5402	TROPICAL SOUTH ATLANTIC INDEX	887e3bcc-ffd4-4f10-a91c-849783aac709	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TROPICAL SOUTH ATLANTIC INDEX	1
6694	5402	WESTERN HEMISPHERE WARM POOL	309d2897-c74b-4de6-96fc-751a6935d549	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > WESTERN HEMISPHERE WARM POOL	1
6695	5405	ANTARCTIC OSCILLATION	511e6c26-8806-4d88-9763-a136a6957042	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ANTARCTIC OSCILLATION	1
6696	5405	ARCTIC OSCILLATION	98e5a7e4-b946-474a-8214-c1b7b3e5f976	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ARCTIC OSCILLATION	1
6697	5405	ATLANTIC MERIDIONAL MODE	f141c968-94d4-4c42-8877-bbe34bb84b26	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ATLANTIC MERIDIONAL MODE	1
6698	5405	ATLANTIC MULTIDECADAL OSCILLATION LONG VERSION	dcdb6cf1-48a7-488e-aeb8-e6c0b36752d4	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ATLANTIC MULTIDECADAL OSCILLATION LONG VERSION	1
6699	5405	BIVARIATE ENSO TIMESERIES INDEX	a69f9faf-f730-4eba-9e38-0f72b0544bbe	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > BIVARIATE ENSO TIMESERIES INDEX	1
6700	5405	BLOCKING INDEX	2aeb8e10-b7f8-429e-b9f6-968ece330741	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > BLOCKING INDEX	1
6701	5405	EAST ATLANTIC JET PATTERN	47fb8f57-2ddd-4289-b8a5-af7ffa0ee031	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EAST ATLANTIC JET PATTERN	1
6702	5405	EAST ATLANTIC PATTERN	64d4ff80-59bb-4565-8759-e5223939abfd	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EAST ATLANTIC PATTERN	1
6703	5405	EASTERN ATLANTIC WESTERN RUSSIA PATTERN	c58e035f-87c6-4aa5-8729-5a9c6270e73b	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EASTERN ATLANTIC WESTERN RUSSIA PATTERN	1
6704	5405	EASTERN PACIFIC OSCILLATION	0384fecd-9303-47f3-84e3-f01f58013fc3	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EASTERN PACIFIC OSCILLATION	1
6705	5405	EL NINO SOUTHERN OSCILLATION (ENSO)	095a05c0-6220-4abd-9c1b-c4504a092d7d	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EL NINO SOUTHERN OSCILLATION (ENSO)	1
6706	5405	EQUATORIAL PACIFIC MERIDIONAL WIND ANOMALY INDEX	21389c4a-0d32-484a-95b9-db319a18f6ca	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EQUATORIAL PACIFIC MERIDIONAL WIND ANOMALY INDEX	1
6707	5405	EQUATORIAL PACIFIC ZONAL WIND ANOMALY INDEX	57a381ef-56f6-48af-8974-822f5859979d	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EQUATORIAL PACIFIC ZONAL WIND ANOMALY INDEX	1
6708	5405	GLOBALLY INTEGRATED ANGULAR MOMENTUM	523c148f-bb4f-47d0-b176-0949ed59288a	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > GLOBALLY INTEGRATED ANGULAR MOMENTUM	1
6709	5405	MADDEN-JULIAN OSCILLATION	25d4368e-3b66-40d5-bac1-2343b127fa32	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > MADDEN-JULIAN OSCILLATION	1
6710	5405	MULTIVARIATE ENSO INDEX	caddaef6-1a60-490a-938e-9107885f286f	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > MULTIVARIATE ENSO INDEX	1
6711	5405	NORTH ATLANTIC OSCILLATION	c5e1c055-768e-4aa3-a0a1-3adfda8ecdca	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH ATLANTIC OSCILLATION	1
6712	5405	NORTH PACIFIC OSCILLATION	2295728d-0ee0-4c6f-9bb4-261b4b22322e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH PACIFIC OSCILLATION	1
6713	5405	NORTH PACIFIC PATTERN	c6abcc08-7d59-4852-8c1a-82f464900333	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH PACIFIC PATTERN	1
6714	5405	NORTHERN OSCILLATION INDEX	77b2422e-ce52-465f-8841-5d04ebe536dc	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTHERN OSCILLATION INDEX	1
6715	5405	PACIFIC DECADAL OSCILLATION	2de06b90-4abe-4c71-a537-978679bf8aea	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > PACIFIC DECADAL OSCILLATION	1
6716	5405	PACIFIC/NORTH AMERICAN (PNA) PATTERN	0e53e397-7836-45ec-bc62-0d54f9f176e5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > PACIFIC/NORTH AMERICAN (PNA) PATTERN	1
6717	5405	Pacific Transition Index	233903dd-daec-474f-ac2e-cdcad84a85b5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > Pacific Transition Index	1
6718	5405	QUASI-BIENNIAL OSCILLATION	ea64fa04-2822-4cc5-9014-f18ce1a1ef23	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > QUASI-BIENNIAL OSCILLATION	1
6719	5405	SOUTHERN OSCILLATION INDEX	eaa0bc43-e283-4bf1-ba20-ca32850a66ef	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > SOUTHERN OSCILLATION INDEX	1
6720	5405	TROPICAL/NORTHERN HEMISPHERE PATTERN	83b711e1-3fb5-4ef3-bafb-783e8239a4b5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > TROPICAL/NORTHERN HEMISPHERE PATTERN	1
6721	5405	WEST PACIFIC INDEX	bdb6eafa-f4e1-4536-b513-4c787f829722	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > WEST PACIFIC INDEX	1
6722	5407	HIGHER MAXIMUM DAYTIME TEMPERATURES	3d997f01-8987-4fb1-a32e-d88d51f0a2c4	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > HIGHER MAXIMUM DAYTIME TEMPERATURES	1
6723	5407	HIGHER MINIMUM NIGHTTIME TEMPERATURES	93741006-ff2a-4ec2-bbd4-ff55301fabe0	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > HIGHER MINIMUM NIGHTTIME TEMPERATURES	1
6724	5407	STRATOSPHERIC TEMPERATURE ANOMALIES	0eb1af15-7bd4-40c6-b8a4-666cbb61ff8c	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > STRATOSPHERIC TEMPERATURE ANOMALIES	1
6725	5407	TEMPERATURE TRENDS	ae247e59-db82-45ac-a9de-a9773ae4db40	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > TEMPERATURE TRENDS	1
6726	5407	TEMPERATURE VARIABILITY	7013bdc9-519d-42b6-827c-4b8013fbb726	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > TEMPERATURE VARIABILITY	1
6727	5407	TROPOSPHERIC TEMPERATURE ANOMALIES	f0e47cca-fa6e-44d0-b900-43920a3d0b91	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICATORS > TROPOSPHERIC TEMPERATURE ANOMALIES	1
6728	5408	COMMON SENSE CLIMATE INDEX	c7fa79e4-67a1-45da-b393-a1b89d54a1a5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > COMMON SENSE CLIMATE INDEX	1
6729	5408	COOLING DEGREE DAYS	db0d03d7-1d08-42fb-b212-0da35b88e656	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > COOLING DEGREE DAYS	1
6730	5408	FREEZING INDEX	bc6d73a9-4943-4a3e-9f9d-9406fa54b0bc	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > FREEZING INDEX	1
6731	5408	GROWING DEGREE DAYS	6d808909-ce04-4401-a883-aff4d723d025	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > GROWING DEGREE DAYS	1
6732	5408	HEATING DEGREE DAYS	fe2bc223-e503-4ca1-924c-d3fd5876721c	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > HEATING DEGREE DAYS	1
6733	5408	RESIDENTIAL ENERGY DEMAND TEMPERATURE INDEX	f19ff7fb-fd8b-433c-88e2-afc5dd3ee7b2	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > RESIDENTIAL ENERGY DEMAND TEMPERATURE INDEX	1
6734	5408	TEMPERATURE CONCENTRATION INDEX (TCI)	d73be111-7aae-4a96-89c2-7b64c064893c	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > TEMPERATURE CONCENTRATION INDEX (TCI)	1
6735	5408	THAWING INDEX	1e540a87-ffd9-4277-b8f2-683a58145b87	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TEMPERATURE INDICES > THAWING INDEX	1
6736	5415	ANIMAL PHENOLOGICAL CHANGES	f73cf4ee-2ae0-47b0-a294-5f8a8f694215	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > PHENOLOGICAL CHANGES > ANIMAL PHENOLOGICAL CHANGES	1
6737	5415	PLANT PHENOLOGICAL CHANGES	c6f81edb-b683-4356-93e6-5852766a5ee8	EARTH SCIENCE > CLIMATE INDICATORS > BIOSPHERIC INDICATORS > PHENOLOGICAL CHANGES > PLANT PHENOLOGICAL CHANGES	1
6738	5427	GLACIER ELEVATION/ICE SHEET ELEVATION	83bd640d-cd05-49a8-9ec7-aab60820b126	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER ELEVATION/ICE SHEET ELEVATION	1
6739	5427	GLACIER FACIES	613c1fba-8710-47fb-a8e1-e4cd50bb97e1	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER FACIES	1
6740	5427	GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	6095d796-68e0-4c7d-aa4f-f2e5bd8c4916	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER MASS BALANCE/ICE SHEET MASS BALANCE	1
6741	5427	GLACIER MOTION/ICE SHEET MOTION	4c9afaf7-4aec-440d-8084-6a482de09e7a	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER MOTION/ICE SHEET MOTION	1
6742	5427	GLACIER/ICE SHEET THICKNESS	6a8a6fdb-c431-4d32-8cea-5849e2ee1f33	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER/ICE SHEET THICKNESS	1
6743	5427	GLACIER/ICE SHEET TOPOGRAPHY	c3e4d439-bbb0-48c9-89eb-57d3a330627a	EARTH SCIENCE > CLIMATE INDICATORS > CRYOSPHERIC INDICATORS > GLACIAL MEASUREMENTS > GLACIER/ICE SHEET TOPOGRAPHY	1
6744	5442	PALMER DROUGHT CROP MOISTURE INDEX	7e26f9e3-4c20-453d-bbc6-1970eca1ffb8	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > DROUGHT INDICES > PALMER DROUGHT CROP MOISTURE INDEX	1
6745	5442	PALMER DROUGHT SEVERITY INDEX	a43850a1-7b00-4993-80ff-753c2b5c4015	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > DROUGHT INDICES > PALMER DROUGHT SEVERITY INDEX	1
6746	5442	PALMER HYDROLOGICAL DROUGHT INDEX	0365f0af-7843-4ba3-af8c-82d032c14f7e	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > DROUGHT INDICES > PALMER HYDROLOGICAL DROUGHT INDEX	1
6747	5442	PALMER Z INDEX	0565650b-dce1-4ae8-8a7a-7ce25ac198c3	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > DROUGHT INDICES > PALMER Z INDEX	1
6748	5447	CROP HARVEST DATES	f5824b8f-c3e7-4e56-96e8-cf4b5adefbf8	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LENGTH OF GROWING SEASON > CROP HARVEST DATES	1
6749	5447	FREEZE/FROST DATE	226d4804-1a09-4d9b-a5c1-346f52a2e709	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LENGTH OF GROWING SEASON > FREEZE/FROST DATE	1
6750	5447	FREEZE/FROST PROBABILITY	efc141a6-7d8e-45d5-b335-2fc122c62d78	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LENGTH OF GROWING SEASON > FREEZE/FROST PROBABILITY	1
6751	5447	LENGTH OF FREEZE FREE PERIOD	738185b7-54d6-41a2-b31f-b8a4ee1dabe7	EARTH SCIENCE > CLIMATE INDICATORS > LAND SURFACE/AGRICULTURE INDICATORS > LENGTH OF GROWING SEASON > LENGTH OF FREEZE FREE PERIOD	1
6752	5457	BIOMARKER	625ac4b3-a126-4c98-a061-3a780b942280	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > BIOMARKER	1
6753	5457	CORAL DEPOSITS	afeb9962-d3e8-4260-ab2b-e62e11099e31	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > CORAL DEPOSITS	1
6754	5457	FAUNA	cffe377f-d840-4bcf-9223-8379b72defe7	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > FAUNA	1
6755	5457	MACROFOSSILS	14c78811-5296-4095-9c44-26362914e798	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > MACROFOSSILS	1
6756	5457	MICROFOSSILS	0aa423e0-bc21-4d74-894d-a0dfcf17fae5	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > MICROFOSSILS	1
6757	5457	PALEOVEGETATION	fbd867cf-f7e8-4dbc-9fd2-2ccc0728350f	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > PALEOVEGETATION	1
6758	5457	POLLEN	59719c53-a2b7-4200-9b3c-dfa5d39607f7	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > POLLEN	1
6759	5457	POPULATION ABUNDANCE	7bc06198-5546-40f5-97ac-b7b5b5503cfc	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > POPULATION ABUNDANCE	1
6760	5457	TREE RINGS	6444fc67-8cad-41c0-9ded-e93f604ba8b0	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > TREE RINGS	1
6761	5458	CARBON DIOXIDE	b53939ae-1264-409d-8434-3bb3d22b2848	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > CARBON DIOXIDE	1
6762	5458	ELECTRICAL PROPERTIES	a2987914-ed66-4b7c-964d-8eccf0174e57	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ELECTRICAL PROPERTIES	1
6763	5458	ICE CORE AIR BUBBLES	42664b0d-26c2-44ad-b0a9-673ed2902f00	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ICE CORE AIR BUBBLES	1
6764	5458	IONS	302d7079-299a-4269-bd7e-d95009c9b46e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > IONS	1
6765	5458	ISOTOPES	a0358b3e-0926-4b17-8b32-c1b15a73cba5	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ISOTOPES	1
6766	5458	METHANE	0948a59e-cc72-4e5d-b97d-4ea0335b0906	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > METHANE	1
6767	5458	NITROUS OXIDE	bc90bc40-2a21-4a6f-9fb9-bf3ae5845157	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > NITROUS OXIDE	1
6768	5458	PARTICULATE MATTER	15fdef7c-7fb7-4a1d-a24b-01164a8ba11a	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > PARTICULATE MATTER	1
6769	5458	VOLCANIC DEPOSITS	c736e45d-63f2-428b-abae-48f79d007703	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > VOLCANIC DEPOSITS	1
6770	5459	BOREHOLES	f1f84fc8-d242-4f97-bb7d-77b68631273e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > BOREHOLES	1
6771	5459	CAVE DEPOSITS	482453d7-ffa4-4ae9-8158-9fa73bcf39ef	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > CAVE DEPOSITS	1
6772	5459	FIRE HISTORY	d2dc2330-0433-43f2-9154-dc399d24406c	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > FIRE HISTORY	1
6773	5459	GLACIAL RETREAT	2f257f83-bddd-41ce-ac78-5dac857b1be3	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > GLACIAL RETREAT	1
6774	5459	GLACIATION	3dfa8dcf-0df2-4654-ae3e-c97586265c3e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > GLACIATION	1
6775	5459	ISOTOPES	7557eddd-db2a-4f39-b1e2-91162f4fc92e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > ISOTOPES	1
6776	5459	LOESS	e0d88b2a-8563-443b-8756-73d744a41ee7	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > LOESS	1
6777	5459	PALEOMAGNETIC DATA	219ba382-6c90-43d2-a6cf-2ddcc358f70e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > PALEOMAGNETIC DATA	1
6778	5459	PALEOSOLS	4fe601b0-314f-4f63-8ec1-3b96cc7263b8	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > PALEOSOLS	1
6779	5459	RADIOCARBON	8f4e90e0-aea0-40cd-b781-a6a69a6e6cb3	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > RADIOCARBON	1
6780	5459	SEDIMENTS	0960827a-ecdb-40a0-babc-fbd6df27bb53	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > SEDIMENTS	1
6781	5459	STRATIGRAPHIC SEQUENCE	d845886d-0c44-4505-b5b9-d3fcd819208e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > STRATIGRAPHIC SEQUENCE	1
7296	6087	FAULT MOVEMENT	51ce7da1-b441-474f-b7e5-cedaa04903f7	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > FAULT MOVEMENT	1
6782	5459	VOLCANIC DEPOSITS	52325c6e-1084-43c1-83b2-278bbe0201c6	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > VOLCANIC DEPOSITS	1
6783	5461	BOREHOLES	8f8c1808-ac5f-43e5-8397-dbb3d171144c	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > BOREHOLES	1
6784	5461	CORAL DEPOSITS	47d6c670-db83-4975-b684-1be787811ac8	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > CORAL DEPOSITS	1
6785	5461	ISOTOPES	dc02e5fb-9ff3-483d-8c33-18db25a07eea	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > ISOTOPES	1
6786	5461	LAKE LEVELS	2c99427c-1a6a-4326-b072-0c12c87bd944	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > LAKE LEVELS	1
6787	5461	MACROFOSSILS	11e12021-f63e-4081-ae78-1bb19fe7b4bf	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > MACROFOSSILS	1
6788	5461	MICROFOSSILS	6d00c961-de64-40ed-becd-3a95cae182e3	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > MICROFOSSILS	1
6789	5461	OXYGEN ISOTOPES	9713a1d5-8b03-4d38-b3b6-34578a1d5f39	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > OXYGEN ISOTOPES	1
6790	5461	PALEOMAGNETIC DATA	7ee90f7c-bdc6-403a-b447-2100d573cad6	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > PALEOMAGNETIC DATA	1
6791	5461	POLLEN	fe06f678-7155-4f93-9e28-4c083d60cccc	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > POLLEN	1
6792	5461	RADIOCARBON	a389bcd6-929d-43ac-9af1-5a20a4ddcbe2	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > RADIOCARBON	1
6793	5461	SEDIMENTS	b3764016-0b5d-48fb-be3e-4f1082cf13e7	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > SEDIMENTS	1
6794	5461	STRATIGRAPHIC SEQUENCE	417a6538-f89e-4f73-a89a-c2e5d2cd7667	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > STRATIGRAPHIC SEQUENCE	1
6795	5461	VARVE DEPOSITS	9db3b1cb-0d3d-4486-bf56-1e96b8691b01	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > VARVE DEPOSITS	1
6796	5463	CARBON DIOXIDE FORCING	e0867ff5-2eb4-4959-b874-ac37c1b407e0	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE FORCING > CARBON DIOXIDE FORCING	1
6797	5463	ORBITAL CHANGE FORCING	7cc62051-537c-4399-b9b9-b59c1a3e0773	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE FORCING > ORBITAL CHANGE FORCING	1
6798	5463	SOLAR FORCING	250ce118-46e7-4dec-9e44-8054c9318cff	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE FORCING > SOLAR FORCING	1
6799	5463	VOLCANIC FORCING	78c47e38-e842-4e31-81b2-44f44c52c692	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE FORCING > VOLCANIC FORCING	1
6800	5464	AIR TEMPERATURE RECONSTRUCTION	89e5b8c9-ef72-4e21-83c8-a7552f6871a4	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > AIR TEMPERATURE RECONSTRUCTION	1
6801	5464	ATMOSPHERIC CIRCULATION RECONSTRUCTION	555b048d-8904-4a62-a85a-3af1aa14674e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > ATMOSPHERIC CIRCULATION RECONSTRUCTION	1
6802	5464	DROUGHT/PRECIPITATION RECONSTRUCTION	06bcba40-6046-4c0e-aa38-8f83410b93f0	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > DROUGHT/PRECIPITATION RECONSTRUCTION	1
6803	5464	GROUND WATER RECONSTRUCTION	9f687ff2-52c0-496b-9a81-503a8c207823	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > GROUND WATER RECONSTRUCTION	1
6804	5464	LAKE LEVEL RECONSTRUCTION	ec4c1ae2-53f4-40ca-b0c3-e145f00e2583	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > LAKE LEVEL RECONSTRUCTION	1
6805	5464	OCEAN SALINITY RECONSTRUCTION	1ba98ab7-dee3-4b15-aea1-179ecd8f6e7d	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > OCEAN SALINITY RECONSTRUCTION	1
6806	5464	SEA LEVEL RECONSTRUCTION	b51093c5-5997-410c-899d-98d15ab5f5cc	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > SEA LEVEL RECONSTRUCTION	1
6807	5464	SEA SURFACE TEMPERATURE RECONSTRUCTION	facdb262-04eb-47f9-b46e-ba7a379722ec	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > SEA SURFACE TEMPERATURE RECONSTRUCTION	1
6808	5464	SEDIMENTS	3b4ea1db-bb93-4eb8-ac08-4880a3a5e6d2	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > SEDIMENTS	1
6809	5464	SOLAR FORCING/INSOLATION RECONSTRUCTION	fec6c2e4-ca15-426a-b344-36bba69e5c1f	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > SOLAR FORCING/INSOLATION RECONSTRUCTION	1
6810	5464	STREAMFLOW RECONSTRUCTION	cde7aacb-0204-4a84-afcb-279cc3d0870c	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > STREAMFLOW RECONSTRUCTION	1
6811	5464	VEGETATION RECONSTRUCTION	c1c1890d-a6b0-4482-836b-a4b8ed0beee8	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > VEGETATION RECONSTRUCTION	1
6812	5469	LENGTH OF THE SOLAR CYCLE	22c14e35-48a4-40b5-a503-add48c2d4cd4	EARTH SCIENCE > CLIMATE INDICATORS > SUN-EARTH INTERACTIONS > SUNSPOT ACTIVITY > LENGTH OF THE SOLAR CYCLE	1
6813	5469	SOLAR FLUX	3b230650-68ff-4e7a-9273-6e0b1083bdfa	EARTH SCIENCE > CLIMATE INDICATORS > SUN-EARTH INTERACTIONS > SUNSPOT ACTIVITY > SOLAR FLUX	1
6814	5480	PERMAFROST TEMPERATURE	d8606e80-3d34-4540-a355-5f99737f7ab7	EARTH SCIENCE > CRYOSPHERE > FROZEN GROUND > PERMAFROST > PERMAFROST TEMPERATURE	1
6815	5490	SNOW GRAIN SIZE	a30b2871-4cdc-418a-b00c-969b50008726	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > FIRN > SNOW GRAIN SIZE	1
6816	5499	ICE SHEET MEASUREMENTS	6d6a2b61-5d2c-4ec1-a164-34000f481588	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ICE SHEETS > ICE SHEET MEASUREMENTS	1
6817	5499	SURFACE MORPHOLOGY	94402f47-38ea-4798-98da-ea17599e092f	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ICE SHEETS > SURFACE MORPHOLOGY	1
6818	5520	ICE FRACTION	a3f36d7c-4eed-4d7a-8902-a5fcdc1b6261	EARTH SCIENCE > CRYOSPHERE > SEA ICE > SEA ICE CONCENTRATION > ICE FRACTION	1
6819	5537	BIDIRECTIONAL REFLECTANCE DISTRIBUTION FUNCTION	2dce1d90-f958-4e96-b8d8-c8b0bc69d16e	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > REFLECTANCE > BIDIRECTIONAL REFLECTANCE DISTRIBUTION FUNCTION	1
6820	5545	SPECIFIC SURFACE AREA	a72b96ad-3755-4205-b353-66592c7bff54	EARTH SCIENCE > CRYOSPHERE > SNOW/ICE > SNOW MICROSTRUCTURE > SPECIFIC SURFACE AREA	1
6821	5553	COUNTRY BOUNDARIES	245c630a-8022-46ed-9a79-8f6cf99b0822	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES > POLITICAL DIVISIONS > COUNTRY BOUNDARIES	1
6822	5553	STATE BOUNDARIES	ef04f170-4797-4db1-aff7-ad493b6a7cda	EARTH SCIENCE > HUMAN DIMENSIONS > BOUNDARIES > POLITICAL DIVISIONS > STATE BOUNDARIES	1
6823	5554	MONOCULTURE	941c691a-3bff-4c58-854a-16c5529524e9	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > AGRICULTURE PRODUCTION > MONOCULTURE	1
6824	5556	BIOMASS ENERGY PRODUCTION/USE	99ed30c9-332c-4acf-8620-eab3c67bcc90	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > BIOMASS ENERGY PRODUCTION/USE	1
6825	5556	COAL PRODUCTION/USE	c90081fb-f6c2-4f7c-a124-0cd432e92200	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > COAL PRODUCTION/USE	1
6826	5556	GEOTHERMAL ENERGY PRODUCTION/USE	05410006-351a-4877-96e8-f0a821161ecf	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > GEOTHERMAL ENERGY PRODUCTION/USE	1
6827	5556	HYDROELECTRIC ENERGY PRODUCTION/USE	7eba0eef-3a30-4282-a162-1f483370ddc4	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > HYDROELECTRIC ENERGY PRODUCTION/USE	1
6828	5556	HYDROGEN PRODUCTION/USE	c346378a-09ee-428c-89c1-c94354cdc74f	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > HYDROGEN PRODUCTION/USE	1
6829	5556	METHANE PRODUCTION/USE	d3b2e908-b732-480c-a9cb-2e981da52094	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > METHANE PRODUCTION/USE	1
6830	5556	NATURAL GAS PRODUCTION/USE	83bddfa5-d9ba-40f1-9a2f-1bee33559176	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > NATURAL GAS PRODUCTION/USE	1
6831	5556	NUCLEAR ENERGY PRODUCTION/USE	582af998-1f5c-48a7-8cdd-70fe06bb9f17	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > NUCLEAR ENERGY PRODUCTION/USE	1
6832	5556	OIL PRODUCTION/USE	e5d17711-c9c1-42f6-96e4-c618c0df37cb	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > OIL PRODUCTION/USE	1
6833	5556	PETROLEUM PRODUCTION/USE	e4774745-c565-4b9e-a642-6fa4a0b3b79b	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > PETROLEUM PRODUCTION/USE	1
6834	5556	SOLAR ENERGY PRODUCTION/USE	8b4f34c1-7aed-4833-811a-401382abd17c	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > SOLAR ENERGY PRODUCTION/USE	1
6835	5556	TIDAL ENERGY PRODUCTION/USE	1eb6eeff-77f8-40b6-8e4a-2e4438f00b10	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > TIDAL ENERGY PRODUCTION/USE	1
6836	5556	WAVE ENERGY PRODUCTION/USE	62c1fec5-3512-4136-a060-ec2338a48296	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > WAVE ENERGY PRODUCTION/USE	1
6837	5556	WIND ENERGY PRODUCTION/USE	b3a95e10-1c1d-41cf-8802-8bb1d3a41353	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > ENERGY PRODUCTION/USE > WIND ENERGY PRODUCTION/USE	1
6838	5558	ECOTOURISM	e6cf64ce-389f-479c-835a-eecd612d4d88	EARTH SCIENCE > HUMAN DIMENSIONS > ECONOMIC RESOURCES > TOURISM > ECOTOURISM	1
6839	5564	CARBON DIOXIDE REMOVAL	1595c0a9-63a8-433c-8515-044a977d73a7	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > GEOENGINEERING > CARBON DIOXIDE REMOVAL	1
6840	5564	SOLAR RADIATION MANAGEMENT	0f583845-c39e-471d-a590-8212a4358e1e	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > GEOENGINEERING > SOLAR RADIATION MANAGEMENT	1
6841	5565	LAND TENURE	0ceb5ef1-5a07-4f93-8e86-d3cc2baf5768	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > LAND MANAGEMENT > LAND TENURE	1
6842	5565	LAND USE CLASSES	1fd206a9-83a7-4f43-902d-003811080fed	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > LAND MANAGEMENT > LAND USE CLASSES	1
6843	5565	LAND USE/LAND COVER CLASSIFICATION	5066def0-b14b-4a2c-b40f-dc9953860366	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > LAND MANAGEMENT > LAND USE/LAND COVER CLASSIFICATION	1
6844	5567	GROUNDWATER MANAGEMENT	96810430-e7e1-45eb-a4eb-8a7e17fe5076	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > WATER MANAGEMENT > GROUNDWATER MANAGEMENT	1
6845	5567	STORMWATER MANAGEMENT	873e35f5-908b-4418-861e-eab5d13a19a4	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > WATER MANAGEMENT > STORMWATER MANAGEMENT	1
6846	5567	WASTEWATER MANAGEMENT	cbf64c32-99fa-4312-91a0-4fc85a6890bb	EARTH SCIENCE > HUMAN DIMENSIONS > ENVIRONMENTAL GOVERNANCE/MANAGEMENT > WATER MANAGEMENT > WASTEWATER MANAGEMENT	1
6847	5617	CYCLONES	0720043d-4d31-45ae-a37c-9ba5959bf97d	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES > CYCLONES	1
6848	5617	HURRICANES	6314f68a-1f00-4e6d-9f06-b3e2ce4348e8	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES > HURRICANES	1
6849	5617	SEVERE CYCLONIC STORMS	4bee2d4d-d15d-4300-8804-626eff7ac0f3	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES > SEVERE CYCLONIC STORMS	1
6850	5617	SEVERE TROPICAL CYCLONES	6f7996f7-5905-42e7-b9fd-c24c6328b5d9	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES > SEVERE TROPICAL CYCLONES	1
6851	5617	TYPHOONS	bd5c19e4-b25a-48b2-ad9d-4596a0ba67de	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > TROPICAL CYCLONES > TYPHOONS	1
6852	5620	BURNED AREA	436b098d-e4d9-4fbd-9ede-05675e111eee	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > WILDFIRES > BURNED AREA	1
6853	5620	WILDFIRE SUPPRESSION	5e693789-87a8-4f94-9b5d-a50cecf55e24	EARTH SCIENCE > HUMAN DIMENSIONS > NATURAL HAZARDS > WILDFIRES > WILDFIRE SUPPRESSION	1
6854	5621	INFANT MORTALITY RATES	611f0108-5706-43ca-bc39-38e528f6024b	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > MORTALITY > INFANT MORTALITY RATES	1
6855	5621	MORTALITY RATES	918c4136-bb4c-422b-9c15-8273307546d1	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > MORTALITY > MORTALITY RATES	1
6856	5622	NATALITY RATES	d0931461-2e93-418c-b470-a218cadcf498	EARTH SCIENCE > HUMAN DIMENSIONS > POPULATION > NATALITY > NATALITY RATES	1
6857	5628	EPIDEMIOLOGY	b8a877b7-d867-4305-9053-3777e5dd330a	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS > EPIDEMIOLOGY	1
6858	5628	FOODBORNE DISEASES	007eeff3-1c96-4b54-aa35-2de5ebb9971a	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS > FOODBORNE DISEASES	1
6859	5628	VECTOR-BORNE DISEASES	9d92320e-b9b9-4ae8-8394-252eeda7ceb1	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS > VECTOR-BORNE DISEASES	1
6860	5628	WATERBORNE DISEASES	68447296-6019-453b-9684-3cd3ff1530c9	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS > WATERBORNE DISEASES	1
6861	5629	AEROALLERGENS	6984e0a6-cb78-4f60-a31d-3ff8415e3829	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > ENVIRONMENTAL HEALTH FACTORS > AEROALLERGENS	1
6862	5629	PARTICULATE MATTER CONCENTRATIONS	681812bd-c115-42b2-b717-f89715e89406	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > ENVIRONMENTAL HEALTH FACTORS > PARTICULATE MATTER CONCENTRATIONS	1
6863	5629	URBAN HEAT ISLAND	5ce8b673-cdb9-4000-ad00-774d1c67c1b1	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > ENVIRONMENTAL HEALTH FACTORS > URBAN HEAT ISLAND	1
6864	5631	MALNUTRITION RATES	4dcd46e9-4830-4de0-b75a-820729a6d787	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > MALNUTRITION > MALNUTRITION RATES	1
6865	5633	MORBIDITY RATES	4b95ab99-4784-44aa-99f0-ecc677dbda65	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > MORBIDITY > MORBIDITY RATES	1
6866	5671	DUNES	416221ec-04e1-4913-aacb-9045551949c4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES	1
6867	5671	RIPPLES	1376f8a1-84f2-4797-a978-69ec520e2423	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > RIPPLES	1
6868	5672	ABRASION	eb039da2-8af7-4d31-9ec9-0700251cfd5d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION	1
6869	5672	DEFLATION	03ea18fe-793d-48e0-aa44-e211376c73d8	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > DEFLATION	1
6870	5672	DEGRADATION	32f6083c-f6a2-40cf-8cf4-782b02b9df9e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > DEGRADATION	1
6871	5672	SALTATION	cfaf76ef-89e2-4dc8-a4eb-b3308ef8c52c	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SALTATION	1
6872	5672	SEDIMENT TRANSPORT	0b5e5a9b-5552-4e41-b1a1-9c01c52dff4b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT	1
6873	5672	SEDIMENTATION	5fff607c-5df4-4f06-a541-896f7cbc1e4c	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION	1
6874	5672	WEATHERING	82eac236-38ba-469d-837a-950ffa7e8316	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > WEATHERING	1
6875	5673	BARRIER ISLANDS	128db882-0522-4a5e-ac69-81d05986a645	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > BARRIER ISLANDS	1
6876	5673	BEACHES	68b4238d-c10f-4f59-9c23-820563107d12	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > BEACHES	1
6877	5673	CORAL REEFS	c6244bfb-300f-4818-bf45-cf1a15e7e073	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS	1
6878	5673	CUSPATE FORELANDS	11175bd5-ee63-4b13-aa03-bc5500a458c2	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CUSPATE FORELANDS	1
6879	5673	DELTAS	93647a7c-a881-4066-a696-c19053c7c30b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DELTAS	1
6880	5673	DUNES	362993fc-743e-42bc-a011-459baea8f427	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES	1
6881	5673	ESTUARIES	8d634619-aed2-4326-a73d-cec49ff74398	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > ESTUARIES	1
6882	5673	FJORDS	7299f45f-eafb-4ed9-ae12-5e01c97c1530	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > FJORDS	1
6883	5673	HEADLANDS/BAYS/CAPE	153080e1-2ab1-438a-8f1e-0cb6d5fe1242	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > HEADLANDS/BAYS/CAPE	1
6884	5673	INLETS	49db8758-1282-45a0-ad3f-0f1e9d8abc44	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > INLETS	1
6885	5673	ISTHMUS	e069e3fc-0c75-40ee-92d7-595991f8fdb4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > ISTHMUS	1
6886	5673	LAGOONS	d9483208-ff59-4293-9867-3f4895e58c9f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > LAGOONS	1
6887	5673	RIA	1e7daefd-fa73-4561-90cc-478ca37bcb9a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > RIA	1
6888	5673	SALT MARSH	d541e4e1-2542-4716-b943-e080b0865e74	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SALT MARSH	1
6889	5673	SEA ARCHES	575d5577-3107-4192-83a3-5a28ceea7a5d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA ARCHES	1
6890	5673	SEA CAVES	c702cd1d-48dd-4652-9ec6-cff6ff52b430	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA CAVES	1
6891	5673	SEA CLIFFS	a82477e6-b563-4135-90e8-c6977c7381be	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA CLIFFS	1
6892	5673	SHOALS	cae5bafd-10a7-4bcf-af1a-3e187ee5e955	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SHOALS	1
6893	5673	SHORELINES	4e5cf935-cf17-4947-bd1f-6816a855953a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SHORELINES	1
6894	5673	SOUNDS	1815faf3-2411-4d2a-a3d5-1e5b0c50782b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SOUNDS	1
6895	5673	SPITS AND BARS	4f25c039-56b9-47a9-9232-d80860da5990	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SPITS AND BARS	1
6896	5673	TOMBOLOS	320e14a6-4882-4533-b1cf-55d49c8a6b37	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > TOMBOLOS	1
6897	5673	WAVE-CUT NOTCH/PLATFORMS	0c523ed2-d02e-4b02-bf21-2da4e171c959	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > WAVE-CUT NOTCH/PLATFORMS	1
6898	5674	ABRASION	9ca8db82-9230-42e0-ad91-9068bc144855	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ABRASION	1
6899	5674	ACCRETION	ee016b0b-353b-4811-bfc2-5d32aed59f29	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ACCRETION	1
6900	5674	ATTRITION/WEATHERING	4dee8110-972f-4665-bd28-a9e64de21a16	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ATTRITION/WEATHERING	1
6901	5674	CHEMICAL SOLUTION	1e73dd30-abb5-4723-be3e-71706d2b1ea1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > CHEMICAL SOLUTION	1
6902	5674	DEPOSITION	8b99d6c3-1751-43e6-81d1-92a7618cadb3	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > DEPOSITION	1
6903	5674	FLOODING	a2401a77-908f-4c03-abcc-d27d99586967	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > FLOODING	1
6904	5674	HYDRAULIC ACTION	ebb8ef06-0f73-48eb-bc22-47f36a729bc6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > HYDRAULIC ACTION	1
6905	5674	SALTATION	c344fddc-ffa8-4093-bcf5-bcfe7806c737	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SALTATION	1
6906	5674	SEA LEVEL CHANGES	2aad0e7e-1c96-4d87-adeb-4894225e2922	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEA LEVEL CHANGES	1
6907	5674	SEDIMENT TRANSPORT	5e101ced-5d9f-4733-8768-38db92d83660	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENT TRANSPORT	1
6908	5674	SEDIMENTATION	866aa07b-132c-4b93-9ced-d74b56b3016f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION	1
6909	5674	SUBMERGENCE	43b2798d-32ac-497f-8881-98d52422e3ac	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUBMERGENCE	1
6910	5674	SUBSIDENCE	af017320-085a-4e6c-81c2-38056cb55c7b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUBSIDENCE	1
6911	5674	SUSPENSION	62ecfc64-48d0-4373-9c44-599471703cf4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUSPENSION	1
6912	5674	WAVE BREAKING	406bfa8b-8522-4776-936a-1fda8b0cfe97	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE BREAKING	1
6913	5674	WAVE DIFFRACTION	ab0138b8-6939-4ac1-aa5f-36073d52360b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE DIFFRACTION	1
6914	5674	WAVE EROSION	097a7f54-df6e-4aeb-8d15-65d4bd24da64	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE EROSION	1
6915	5674	WAVE REFRACTION	df4a0112-3aba-41ca-816a-86129cacb6a5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE REFRACTION	1
6916	5674	WAVE SHOALING	15d5b23c-f739-43b5-bf14-3063c0a59f2d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE SHOALING	1
6917	5675	AIT	3207af29-bd29-4f85-9a08-2614579dd27f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > AIT	1
6918	5675	BAR	ff850d62-675c-4386-a375-fe4af92ec3ff	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > BAR	1
6919	5675	BAYOU	a6fdb3c7-a0ea-4f7c-82e5-d72db09b6444	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > BAYOU	1
6920	5675	CANYON	a78c946a-9529-4643-b002-1aa2ac9cfed6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CANYON	1
6921	5675	CONFLUENCE	e18c970a-d0c6-4430-b419-64cf718bc456	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CONFLUENCE	1
6922	5675	CUTBANK	47ea7cc6-2816-4d64-ad41-6ac1d11c2a33	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CUTBANK	1
6923	5675	DELTAS	daa297ec-4397-4caa-b563-634a71f62b8a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > DELTAS	1
6924	5675	ENDORHEIC BASIN	1afe698e-d920-4756-8de4-482d2ef15a24	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > ENDORHEIC BASIN	1
6925	5675	FLOOD PLAIN	ba37314d-ec38-4e67-bf30-7e1fdc6bfbad	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > FLOOD PLAIN	1
6926	5675	GULLY	b9b85df8-3b95-4baf-bd32-8bacd35dc9b5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > GULLY	1
6927	5675	ISLAND	9d078d5c-62cb-46b5-a6f5-43678643a0ce	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > ISLAND	1
6928	5675	LACUSTRINE PLAIN	8ca51b5e-0b7a-4b7a-b7e2-6e163e195e26	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > LACUSTRINE PLAIN	1
6929	5675	MARSH	4c09d43f-68d5-469d-aaed-f9ef8968ef2e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > MARSH	1
6930	5675	MEANDER	b976b8e5-01b9-4bb3-ba4c-308f8fa0fb97	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > MEANDER	1
6931	5675	OX-BOW LAKE	c5a9eb49-93c4-4fb5-9a02-5fa06ea8800f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > OX-BOW LAKE	1
6932	5675	PINGO	71b4e773-40a4-47db-8449-7c13f4cc49d9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > PINGO	1
6933	5675	POINT BAR	00e49fcb-d846-4b4e-8f45-b022c1713920	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > POINT BAR	1
6934	5675	POND	89228e69-5a64-4662-839f-cb3d2209fa41	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > POND	1
6935	5675	RIFFLE	af058c0e-d40b-4e59-9f92-67b59fd1e2bd	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > RIFFLE	1
6936	5675	RIVER	87624706-e11f-4043-ac54-479ed94b8dac	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > RIVER	1
6937	5675	SPRING	620a9e6c-5851-48b7-93c5-a1706546f5d1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > SPRING	1
6938	5675	STREAM TERRACE	d1964724-2481-417a-be5a-e0dedb111ab4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > STREAM TERRACE	1
6939	5675	STREAM	01a84bc1-a571-4d23-b57f-1b04fd9542a6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > STREAM	1
6940	5675	SWAMP	8f6adff6-672d-4066-8c85-25418a7d0e00	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > SWAMP	1
6941	5675	VALLEY	f4f9c238-2d7e-4529-944b-52389c13932c	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > VALLEY	1
6942	5675	WATERFALL	97c6eb84-90a8-4b47-9a22-99c7c1369989	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > WATERFALL	1
6943	5675	WATERSHED/DRAINAGE BASIN	feceb3aa-d3b4-49e0-ad85-3275acd604fb	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > WATERSHED/DRAINAGE BASIN	1
6944	5676	ABRASION	6ae0d1f7-cc99-4da7-8446-e2dca16f546b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ABRASION	1
6945	5676	ATTRITION	b655ca30-361c-4434-a784-68b8ab99668d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ATTRITION	1
6946	5676	DEGRADATION	ae368822-4979-4feb-967b-ee7764639646	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > DEGRADATION	1
6947	5676	DOWNCUTTING	0bb77741-598a-4f8c-8ce9-5aa0d61a0906	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > DOWNCUTTING	1
6948	5676	ENTRAINMENT	3288c7e0-20fa-4e05-80fa-cdb14c436c7e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ENTRAINMENT	1
6949	5676	HYDRAULIC ACTION	b13bf33a-2a06-489f-80ca-0c77b08588ec	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > HYDRAULIC ACTION	1
6950	5676	LANDSLIDES	c09cb9dc-2916-40f0-9f2f-4bbb39d2e7c9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > LANDSLIDES	1
6951	5676	SALTATION	e8ba38ce-fc48-44b7-8b78-03b69e068d46	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SALTATION	1
6952	5676	SEDIMENT TRANSPORT	4a031bdf-a6c6-40b8-9c92-34cd83a5739e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENT TRANSPORT	1
6953	5676	SEDIMENTATION	b1de8d2f-cfe6-4358-a4cd-5b7e19d0e585	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION	1
6954	5676	SUSPENSION	26352dff-a48b-4b4a-a442-3b5039cf55c0	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SUSPENSION	1
6955	5676	WEATHERING	5d05853c-b709-484f-a406-03f64e643ea4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > WEATHERING	1
6956	5677	ARETES	d37d51e0-1bef-473a-9221-6713166762f9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ARETES	1
6957	5677	CIRQUES/COMBES	b3032f74-fcdf-41d7-8899-2f2b140209c9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CIRQUES/COMBES	1
6958	5677	CREVASSES	b1d30791-5871-474f-aedf-2d4aa51e2b92	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES	1
6959	5677	DRUMLINS	614309a2-4332-4695-aa77-d11794fe4733	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > DRUMLINS	1
6960	5677	ESKERS	158a8764-a6e4-4d28-a1b9-b2ab91e09995	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ESKERS	1
6961	5677	FJORDS	666d9a2b-aaa8-4789-a9d9-a6774e650fe4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > FJORDS	1
6962	5677	GLACIAL HORNS	8c878cc0-d601-4371-af35-9db2c67d8de6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIAL HORNS	1
6963	5677	GLACIER STRIATIONS/GROOVES	c8ad9c7e-384d-42c9-a75c-813a67e4dbfa	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER STRIATIONS/GROOVES	1
6964	5677	GLACIER/HANGING/U-SHAPED VALLEYS	7335b131-0e86-41b3-a0bc-b28120a0a78a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER/HANGING/U-SHAPED VALLEYS	1
6965	5677	GLACIER/ICE CAVES	0a009cb2-9883-48d3-8b91-21efb75b4347	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER/ICE CAVES	1
6966	5677	ICE-DAMMED LAKES	86c6042a-b7ca-4d97-b9d7-db22b1560810	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ICE-DAMMED LAKES	1
6967	5677	KAME DELTA	6a8d6d83-1a3b-452c-90b8-f37b28bd7eb6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KAME DELTA	1
6968	5677	KAMES	a3407182-6908-4206-b2fd-4c39da4072ce	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KAMES	1
6969	5677	KETTLE HOLES	0557b602-cf85-4b04-82a7-ca76f364e5f4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KETTLE HOLES	1
6970	5677	MORAINES	2575cfaf-1a09-48b6-acb9-fda23b6f4719	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES	1
6971	5677	NUNATAKS	12e5921b-0d9b-4656-8d5c-d73abcf90a81	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > NUNATAKS	1
6972	5677	OUTWASH FANS/PLAINS	2e62a5dd-5ea5-4cd6-8051-b5e162ef4e01	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > OUTWASH FANS/PLAINS	1
6973	5677	ROCHE MOUTONNEES/SHEEPBACK	e96cea31-2bee-4d9d-bf4a-d0f469aa3bd4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ROCHE MOUTONNEES/SHEEPBACK	1
6974	5677	ROCK GLACIERS	fcbf8f96-ac53-41b6-9c98-a87425a4ec82	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ROCK GLACIERS	1
6975	5677	TILL PLAINS	bffac466-83aa-4060-a378-6d2d6e49f2a1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > TILL PLAINS	1
6976	5678	ABLATION	ad793d5e-b75d-4d3e-a542-ad4b4075b141	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ABLATION	1
6977	5678	ABRASION	c4c96fc4-c75b-4e98-852d-b28fdf6b77a4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ABRASION	1
6978	5678	CRUST REBOUND	df77e4c7-0b22-4f14-afa5-11b1d335a315	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > CRUST REBOUND	1
6979	5678	DEGRADATION	eb31cb40-97cf-4445-8abd-d375391edf6f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > DEGRADATION	1
6980	5678	DUMPING	45ee1fde-6b00-4aca-ac1b-6c13e2361467	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > DUMPING	1
6981	5678	ENTRAINMENT	10ec2826-c4ac-4373-ad05-9bb4eb35b360	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ENTRAINMENT	1
6982	5678	FIRN FORMATION	e2ea5b37-7004-4943-ad69-ca39a57569a4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FIRN FORMATION	1
6983	5678	FREEZE/THAW	24b052b6-5996-496d-9e91-1fdbda5897da	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FREEZE/THAW	1
6984	5678	GLACIAL DISPLACEMENT	aa74db50-4ae7-463b-903a-2a256f967ca8	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL DISPLACEMENT	1
6985	5678	GLACIAL DRIFT	b313436f-d925-48b7-a339-e6a08475b6e1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL DRIFT	1
6986	5678	GLACIAL GROWTH	6743ea28-0a6e-4d47-ac71-0c9cdf24ac25	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL GROWTH	1
6987	5678	GLACIAL STRIATION	12bb9ec2-a706-436d-aa29-253495276052	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL STRIATION	1
6988	5678	GLACIER CRUST SUBSIDENCE	f8b73efd-d313-41d8-995a-49b80bc8f248	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIER CRUST SUBSIDENCE	1
6989	5678	PERIGLACIAL PROCESSES	2f8b965f-0a0e-427f-a696-ac6b4323744e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > PERIGLACIAL PROCESSES	1
6990	5678	PLUCKING	53e26c7c-5e85-4dd0-a999-8de519bf9976	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > PLUCKING	1
6991	5678	SCOURING	92e348f3-9e6c-4e9e-a1bc-ee72d04755d6	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SCOURING	1
6992	5678	SEDIMENT TRANSPORT	8c6d4f39-6ae0-4c8d-ad48-2f82bb4e1541	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENT TRANSPORT	1
6993	5678	SEDIMENTATION	b609e525-db71-4634-b569-f8aab5ad544e	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION	1
6994	5678	WEATHERING	07825acf-619a-4689-b1ed-09c15166624c	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > WEATHERING	1
6995	5679	CAVES	cdeff06c-28ec-4a4c-b522-4a46f1f9a239	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > CAVES	1
6996	5679	COCKPIT/TOWER KARST	ee347068-e1ff-4271-8726-8343f4f15614	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > COCKPIT/TOWER KARST	1
6997	5679	KARST VALLEY	c9323363-ea07-479d-8b64-e3dbf298a7c5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > KARST VALLEY	1
6998	5679	SINKHOLES (DOLINES)	b9e8b2e3-ea76-4ce9-8a25-64ba0cdef913	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > SINKHOLES (DOLINES)	1
6999	5679	UVALA	d42a8f13-c438-4794-9f37-bd7870ec731d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > UVALA	1
7000	5680	CAC03	50fd29da-a846-4dd6-98e8-e826b75eeda7	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > CAC03	1
7001	5680	DISSOLVED CO2	c2920f06-fd42-47da-9989-3104f8fb7282	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > DISSOLVED CO2	1
7002	5680	KARST HYDROLOGY	e657b41f-4aa0-4816-b3c8-5b477812a0bc	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > KARST HYDROLOGY	1
7003	5680	POROSITY	0317caf8-af0a-4abe-89fb-fd1d9c33b9e7	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > POROSITY	1
7004	5680	WEATHERING	d727d3c7-3a02-48c6-ab63-a4b3d3364783	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > WEATHERING	1
7005	5681	CALDRA	1a0e7a60-9c22-40c5-8424-55119b4db743	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > CALDRA	1
7006	5681	CINDER CONE	a9f7bee8-fb32-40b1-9936-ecf6f6597b6b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > CINDER CONE	1
7007	5681	FAULTS	181fb5a4-125b-445d-b65f-adf9a919c800	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > FAULTS	1
7008	5681	FOLDS	12d2d3ab-2f04-436f-abd4-e28517e6f86c	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > FOLDS	1
7009	5681	GEYSER	1a888a27-8715-46c8-9e11-a6bffba00078	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > GEYSER	1
7010	5681	GRABEN	f1fa2b28-dc04-4373-a6b6-bbcedfaabfb5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > GRABEN	1
7011	5681	HORST	8493f8c2-63c3-4e1c-b813-1f0f3893a30a	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > HORST	1
7012	5681	LAVA DOME	78200b25-8c91-4f1b-82cc-ed79764cd647	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > LAVA DOME	1
7013	5681	LAVA PLAIN	edb9d13d-27a1-4e9a-a32e-4e49b5e76836	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > LAVA PLAIN	1
7014	5681	MAAR	b7ff366c-4322-47bf-b12e-c3fbfb05cf54	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > MAAR	1
7015	5681	MOUNTAINS	8b7f66ea-d481-4641-9dbf-da90ca3ad9c9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > MOUNTAINS	1
7016	5681	PLATEAU	694e18ec-ceaf-4070-9763-f3ee6dbd6b5b	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > PLATEAU	1
7017	5681	RIDGE	97298feb-6991-4d68-8337-177460e436ad	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > RIDGE	1
7018	5681	RIFT VALLEY	ca874a66-f3a8-4099-978c-4684944dc348	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > RIFT VALLEY	1
7019	5681	TUYA	f8a9104b-fe7b-4a60-94fc-6b5ef504db55	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > TUYA	1
7020	5681	VOLCANO	7c2e1960-ae20-46a9-acf1-a3e71542fbb4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > VOLCANO	1
7021	5682	EPEIROGENIC MOVEMENT	bb554660-d608-467c-b265-b9b68eecfb37	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > EPEIROGENIC MOVEMENT	1
7022	5682	ISOSTATIC UPLIFT	4f0f52fb-b272-49c6-9425-690d9285c380	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > ISOSTATIC UPLIFT	1
7023	5682	OROGENIC MOVEMENT	f486acc8-0d0c-4322-bf5c-177bc632bd76	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > OROGENIC MOVEMENT	1
7024	5682	RIFTING	1b370af4-1887-4e7a-82a6-9acb9ce5dd5f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > RIFTING	1
7025	5682	SUBDUCTION	0d43cb88-dd6d-40ac-b241-b628a39ed2af	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > SUBDUCTION	1
7026	5682	TECTONIC UPLIFT	7d5472ba-ae65-45df-a19a-c762055eaead	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > TECTONIC UPLIFT	1
7027	5686	VEGETATION INDEX	e63844c1-015c-4776-b01c-e3e7d5dd3d0c	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND USE/LAND COVER CLASSIFICATION > VEGETATION INDEX	1
7028	5749	BED ELEVATION	05e52e24-b9ac-42cf-bdf9-1dcad56900e8	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TERRAIN ELEVATION > BED ELEVATION	1
7029	5749	CONTOUR MAPS	120f9132-a756-4f6f-a74c-78e94dfcd2a1	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TERRAIN ELEVATION > CONTOUR MAPS	1
7030	5749	DIGITAL ELEVATION/TERRAIN MODEL (DEM)	395372ad-2883-4b6a-a481-6383a310ca47	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TERRAIN ELEVATION > DIGITAL ELEVATION/TERRAIN MODEL (DEM)	1
7031	5749	TOPOGRAPHICAL RELIEF MAPS	f7d2e34a-c5c2-4c21-9132-2472620dbda1	EARTH SCIENCE > LAND SURFACE > TOPOGRAPHY > TERRAIN ELEVATION > TOPOGRAPHICAL RELIEF MAPS	1
7032	5754	COASTAL BATHYMETRY	d80c015f-a383-4883-8309-6aab1c39f5b6	EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > BATHYMETRY > COASTAL BATHYMETRY	1
7033	5766	CORAL BLEACHING	f5df87b6-ed50-4da0-9ba5-7ce4c907bdb3	EARTH SCIENCE > OCEANS > COASTAL PROCESSES > CORAL REEFS > CORAL BLEACHING	1
7034	5851	CHLOROPHYLL	37669b8c-1940-4330-b4e9-ee49ad3673b5	EARTH SCIENCE > OCEANS > OCEAN CHEMISTRY > PIGMENTS > CHLOROPHYLL	1
7035	6033	HYDROGEN GAS VERTICAL/GEOGRAPHIC DISTRIBUTION	833b6958-fc93-473c-aadb-bb65da7578e5	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > HYDROGEN GAS > HYDROGEN GAS VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7036	6034	NATURAL GAS VERTICAL/GEOGRAPHIC DISTRIBUTION	58769369-608c-4482-924b-207454a5fb1c	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > NATURAL GAS > NATURAL GAS VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7037	6035	MICROFOSSIL	37f3fdb8-a82f-4bff-bda4-cca12a683d6f	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > PETROLEUM > MICROFOSSIL	1
7038	6035	PETROLEUM VERTICAL/GEOGRAPHIC DISTRIBUTION	f9e3595d-29b6-462a-8eb6-a06e5a02b081	EARTH SCIENCE > SOLID EARTH > EARTH GASES/LIQUIDS > PETROLEUM > PETROLEUM VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7039	6037	CHEMICAL DECOMPOSITION	14d972b3-a587-4994-a021-f1e620b02341	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > BIOGEOCHEMICAL PROCESSES > CHEMICAL DECOMPOSITION	1
7040	6037	HYDROLYSIS	8c6adb44-54c5-42f1-ae19-602e248ff9d9	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > BIOGEOCHEMICAL PROCESSES > HYDROLYSIS	1
7041	6037	NITRIFICATION	d73ed320-cd5b-4994-a26a-dac5a2fc394f	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > BIOGEOCHEMICAL PROCESSES > NITRIFICATION	1
7042	6038	BIODEGRATION	3e934184-42bd-45ff-b9c1-5c5321fd066f	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > BIODEGRATION	1
7043	6038	CARBONATE FORMATION	b2a9741a-f978-46ac-83ad-e92ff07a637c	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > CARBONATE FORMATION	1
7044	6038	CHEMICAL FIXATION	84b29fbe-8200-4d21-a1a3-fe84fa4cb132	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > CHEMICAL FIXATION	1
7045	6038	CHEMICAL WEATHERING	7e140a1e-385d-4dd3-8b08-6239b082e35e	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > CHEMICAL WEATHERING	1
7046	6038	DECOMPOSITION	7b60ab41-92e7-4550-821b-0ab7ebd3d7c8	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > DECOMPOSITION	1
7047	6038	HYDRATION	2b1f870b-c679-4b6d-b02e-3eb005f0648d	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > HYDRATION	1
7048	6038	ION EXCHANGE	ccbf4ef8-955b-4337-a45b-95affc360173	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > ION EXCHANGE	1
7049	6038	MINERAL DISSOLUTION	524cbe78-9c1f-4ef3-8aa9-0481476c253e	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > MINERAL DISSOLUTION	1
7050	6038	OXIDATION/REDUCTION	9c2f3bee-4629-4607-9962-12fe919594a0	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROCESSES > OXIDATION/REDUCTION	1
7051	6039	CHEMICAL CONCENTRATIONS	12ed4fa0-27cc-4e05-a2b7-bbf2fde871f6	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > CHEMICAL CONCENTRATIONS	1
7052	6039	ISOTOPE MEASUREMENTS	849edfe2-9ed7-4211-8f57-9c8ccff0a4ea	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > ISOTOPE MEASUREMENTS	1
7053	6039	ISOTOPE RATIOS	f7998303-d145-452d-bcff-770f62038909	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > ISOTOPE RATIOS	1
7054	6039	ISOTOPES	441ce068-91f2-4412-8893-c0096d8f9079	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > ISOTOPES	1
7055	6039	ISOTOPIC AGE	211d289d-fae7-4815-9f3d-28a5afc7b3a9	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > ISOTOPIC AGE	1
7056	6039	ROCK-EVAL PRYOLYSIS	2dc96cc9-a128-4dc8-b8c8-1d799201b5c6	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > GEOCHEMICAL PROPERTIES > ROCK-EVAL PRYOLYSIS	1
7057	6040	CHEMICAL DECOMPOSITION	4efb531e-3c6c-4469-9215-d55a8a6ce9da	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > MARINE GEOCHEMICAL PROCESSES > CHEMICAL DECOMPOSITION	1
7058	6040	DISSOLUTION	6628bfb9-c0e1-4281-9b1a-d213a9d5b2d8	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > MARINE GEOCHEMICAL PROCESSES > DISSOLUTION	1
7059	6040	MINERAL DISSOLUTION	f956cc7c-da39-4eac-98ab-ba6207181b7d	EARTH SCIENCE > SOLID EARTH > GEOCHEMISTRY > MARINE GEOCHEMICAL PROCESSES > MINERAL DISSOLUTION	1
7060	6041	COUNTRY/REGIONAL COORDINATE REFERENCE SYSTEM	bb5ca226-fdb1-4fab-9988-7486c643635b	EARTH SCIENCE > SOLID EARTH > GEODETICS > COORDINATE REFERENCE SYSTEM > COUNTRY/REGIONAL COORDINATE REFERENCE SYSTEM	1
7061	6041	GLOBAL COORDINATE REFERENCE SYSTEM	e0a2edbb-8a94-4f47-918a-fe9f93aba5f4	EARTH SCIENCE > SOLID EARTH > GEODETICS > COORDINATE REFERENCE SYSTEM > GLOBAL COORDINATE REFERENCE SYSTEM	1
7062	6044	ELECTRICAL ANOMALIES	d55d29e8-9015-4c23-b137-528eb298aa49	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > ELECTRICAL FIELD > ELECTRICAL ANOMALIES	1
7063	6044	ELECTRICAL INTENSITY	84d77f98-d5a2-4da8-9ba6-0b15e082d050	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > ELECTRICAL FIELD > ELECTRICAL INTENSITY	1
7064	6045	GEOMAGNETIC ACTIVITY	2d3d9a57-44e8-43c0-98b4-b4891c994862	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC FORECASTS > GEOMAGNETIC ACTIVITY	1
7065	6045	GEOMAGNETIC STORM CATEGORY	4b7decec-e378-4824-aecf-9fe509392efd	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC FORECASTS > GEOMAGNETIC STORM CATEGORY	1
7066	6045	TOTAL INTENSITY	9a46a62c-952d-4253-8249-7375c14068a2	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC FORECASTS > TOTAL INTENSITY	1
7067	6046	AA INDEX	5fd5ccc2-5edb-4823-940d-03a290a5c5fc	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES > AA INDEX	1
7068	6046	AE INDEX	31f77d6b-72f7-45e6-93be-8ac5fd5dc373	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES > AE INDEX	1
7069	6046	AM INDEX	b3283844-d867-4c2f-9917-a72bc06fd9ef	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES > AM INDEX	1
7070	6046	DST INDEX	cdb4b514-75c4-4a1f-a4ad-1855fbd396ab	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES > DST INDEX	1
7071	6046	KP INDEX	40386eea-beb0-4b83-906b-75c6bfa24b73	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > GEOMAGNETIC INDICES > KP INDEX	1
7072	6047	GEOMAGNETIC INDUCTION	ee421700-0fe2-420c-9a07-91e8ae9fb524	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD > GEOMAGNETIC INDUCTION	1
7073	6047	MAGNETIC ANOMALIES	65ae8ab2-489b-44bf-bf5b-43cf957b70c0	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD > MAGNETIC ANOMALIES	1
7074	6047	MAGNETIC DECLINATION	f311eac7-5c85-4a8f-90c2-abcff3eec92d	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD > MAGNETIC DECLINATION	1
7075	6047	MAGNETIC INCLINATION	f0b7311e-df08-45fa-8dd5-33b6f74a66d9	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD > MAGNETIC INCLINATION	1
7076	6047	MAGNETIC INTENSITY	d817911a-685b-4c9f-bdc7-2411b8c0a7af	EARTH SCIENCE > SOLID EARTH > GEOMAGNETISM > MAGNETIC FIELD > MAGNETIC INTENSITY	1
7077	6050	DUNES	e43473a1-4392-48e3-9e56-8a4dcad8d7a2	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES	1
7078	6050	RIPPLES	cae41424-161f-4378-a1a4-62cd76c61143	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > RIPPLES	1
7079	6051	ABRASION	f6e19e2e-555a-4d40-9833-c7513d92c813	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION	1
7080	6051	DEFLATION	d415cb15-7586-464c-8707-9a5623a61cee	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > DEFLATION	1
7081	6051	DEGRADATION	baf70c0f-fd59-4d4b-ae03-b664e0352ff7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > DEGRADATION	1
7082	6051	SALTATION	78778362-5d08-4cd7-9131-159cad561e54	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SALTATION	1
7083	6051	SEDIMENT TRANSPORT	fe2d9f93-ee9c-4d1e-af28-0c15ee762019	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT	1
7084	6051	SEDIMENTATION	22ba30ec-a4e2-4547-bad7-4d5f9917625d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION	1
7085	6051	WEATHERING	7a67a5af-42be-4aa7-8cb1-e1fc0de074cc	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > WEATHERING	1
7086	6052	BARRIER ISLANDS	6e3135e9-6be6-4995-a5df-022f6a0cf45b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > BARRIER ISLANDS	1
7087	6052	BEACHES	6a5d3e4d-86d1-4863-bfe6-f8e2899fab0e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > BEACHES	1
7088	6052	CORAL REEFS	dff4d4af-e1e0-4991-884b-a1c088a802b2	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS	1
7089	6052	CUSPATE FORELANDS	0c51bdb0-54b0-4d0d-afd0-35ef7458ccb7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CUSPATE FORELANDS	1
7090	6052	DELTAS	b37b1bdf-6392-4a80-891a-14f177ba2ca2	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DELTAS	1
7091	6052	DUNES	0c279e58-9ad3-4748-816a-de8cabeaf0c4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES	1
7092	6052	ESTUARIES	127fdf1d-9985-4a27-9b6c-ad54380fd299	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > ESTUARIES	1
7093	6052	FJORDS	c9291bc7-784d-486a-95fa-f08fa1edcad9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > FJORDS	1
7094	6052	HEADLANDS/BAYS/CAPE	860e25fa-e63a-4fd0-bde9-4f596b4a5929	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > HEADLANDS/BAYS/CAPE	1
7095	6052	INLETS	356a245d-418a-4560-9eb1-d12f8f155f66	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > INLETS	1
7096	6052	ISTHMUS	ca9d9064-91c8-4c49-b388-e5f7290a3234	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > ISTHMUS	1
7097	6052	LAGOONS	081d131a-6bef-47dc-adb3-f96da9123f93	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > LAGOONS	1
7098	6052	RIA	8d4c5e9c-bdab-48c9-89da-1eb4b9a528ab	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > RIA	1
7099	6052	SALT MARSH	85f409fd-9d81-4cac-84ed-fb0bb4599924	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SALT MARSH	1
7100	6052	SEA ARCHES	4321cb64-0997-438f-92fb-45169503c01f	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA ARCHES	1
7101	6052	SEA CAVES	521f883e-18be-4f28-b5fe-c1f887b4233a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA CAVES	1
7102	6052	SEA CLIFFS	01400b09-68a3-4e3e-b076-1687e30bed56	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SEA CLIFFS	1
7103	6052	SHOALS	94b575b8-eac4-433d-aa74-d781b650f452	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SHOALS	1
7104	6052	SHORELINES	57e6b119-567b-44d0-9d93-278ed5c21c47	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SHORELINES	1
7105	6052	SOUNDS	c5b85924-9e3f-4106-b389-1ab4486bd233	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SOUNDS	1
7106	6052	SPITS AND BARS	62ef0883-8311-4485-947a-2691b456b667	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > SPITS AND BARS	1
7107	6052	TOMBOLOS	30f556c4-7531-4758-9e51-8adc6b2e0e8a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > TOMBOLOS	1
7108	6052	WAVE-CUT NOTCH/PLATFORMS	ee1d9786-33e9-46dc-b859-25d18e9c8a88	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > WAVE-CUT NOTCH/PLATFORMS	1
7109	6053	ABRASION	fd29bf77-df38-4b80-8148-8184fa41d843	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ABRASION	1
7110	6053	ACCRETION	8b232049-ce98-4a34-8f00-2366335508e4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ACCRETION	1
7111	6053	ATTRITION/WEATHERING	36b178ad-4f20-41ce-89d1-4ee8567a3cf2	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > ATTRITION/WEATHERING	1
7112	6053	CHEMICAL SOLUTION	bb891ee1-6c7b-4ec0-b2fa-6fb67a2df2a3	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > CHEMICAL SOLUTION	1
7113	6053	DEPOSITION	6a11e5e5-e6a3-42dd-b793-141ce99932e1	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > DEPOSITION	1
7114	6053	FLOODING	fb5c09ec-c924-4deb-8294-8a27697a4550	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > FLOODING	1
7115	6053	HYDRAULIC ACTION	8fde8c6c-97d4-41a6-9e20-f862faafcd88	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > HYDRAULIC ACTION	1
7116	6053	SALTATION	872459ca-da1e-448f-9bf4-383b628f4609	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SALTATION	1
7117	6053	SEA LEVEL CHANGE	6c958ab4-ab98-438e-86d4-1e6a6d0580da	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEA LEVEL CHANGE	1
7118	6053	SEDIMENT TRANSPORT	1088e9e2-dadd-4d20-a2db-ef7df32c6d42	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENT TRANSPORT	1
7119	6053	SEDIMENTATION	2cca0a13-3c6f-4617-aca9-bff7f8142c52	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION	1
7120	6053	SUBMERGENCE	87186c13-548e-4ea8-ba79-38cff394eb59	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUBMERGENCE	1
7121	6053	SUBSIDENCE	b3657e71-acd1-4be4-9c70-a54e074a40a4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUBSIDENCE	1
7122	6053	SUSPENSION	15c6332d-f6f2-45a4-9485-bb55471c0090	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SUSPENSION	1
7123	6053	WAVE BREAKING	a8c37cb5-9426-41fd-b192-53b4c3ae1ba3	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE BREAKING	1
7124	6053	WAVE DIFFRACTION	5cbfc557-f3a6-4558-9954-ce37f0510952	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE DIFFRACTION	1
7125	6053	WAVE EROSION	86405d6d-eb37-4aa5-a525-bf6a23fd131d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE EROSION	1
7126	6053	WAVE REFRACTION	b43d2d47-c86e-41b6-81bd-be803db536da	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE REFRACTION	1
7127	6053	WAVE SHOALING	f8accc20-818e-47a1-962d-80b7ec7f6d92	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE SHOALING	1
7128	6054	AIT	d8b04023-b9c4-42bc-a986-ab6c4f32ba28	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > AIT	1
7129	6054	BAR	6c061296-2c92-4aa4-b9d1-6ecf0efde876	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > BAR	1
7130	6054	BAYOU	244bd4be-a3d2-4c02-b576-ae9f2f9e544f	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > BAYOU	1
7131	6054	CANYON	e25ce36c-eacd-447a-9d73-ccc8a7e3a328	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CANYON	1
7132	6054	CONFLUENCE	cbd9ee43-24f8-45ab-a39b-2ff34be81c51	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CONFLUENCE	1
7133	6054	CUTBANK	8dcff6c3-a6b3-479e-96e2-63191d10ac2d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > CUTBANK	1
7134	6054	DELTAS	ad535c83-3b93-4632-8aaa-7dfba8bb125a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > DELTAS	1
7135	6054	ENDORHERIC BASIN	4a2a2f6d-9735-4bee-9d1a-21dcd0352c6b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > ENDORHERIC BASIN	1
7136	6054	FLOOD PLAIN	d71f94cb-e773-487a-a8ff-9c5f11c1dbc4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > FLOOD PLAIN	1
7137	6054	GULLY	2f8ad9b0-adb8-4022-8c95-bca68e7a87a5	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > GULLY	1
7138	6054	ISLAND	74caea9b-6023-438b-af3d-bb9d948036f1	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > ISLAND	1
7139	6054	LACUSTRINE PLAIN	588d868d-05a4-4dac-9fb3-770b54ce39e5	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > LACUSTRINE PLAIN	1
7140	6054	MARSH	88adcca6-2bc8-443a-9f25-c9aded577615	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > MARSH	1
7141	6054	MEANDER	c6f77e54-069e-454f-8260-e150bc29547a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > MEANDER	1
7142	6054	OX-BOW LAKE	12233807-f6cd-410d-b607-ecbfbd545464	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > OX-BOW LAKE	1
7143	6054	PINGO	4a0c46ff-2d07-442d-b141-6156d9ea4a2e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > PINGO	1
7144	6054	POINT BAR	dd0de414-6663-4280-94cf-bda7fea736cc	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > POINT BAR	1
7145	6054	POND	5f292d99-b14a-4f18-bbe0-8025d04cae50	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > POND	1
7146	6054	RIFFLE	5df6e78f-6dd4-4fc8-a88e-9e575dbca2eb	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > RIFFLE	1
7147	6054	RIVER	bb6b3b76-c496-464b-bd20-1b22296aae15	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > RIVER	1
7148	6054	SPRING	b498a5cb-f77d-4485-8174-81dec28cee0e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > SPRING	1
7149	6054	STREAM TERRACE	74ce5e8a-038a-471e-a27a-be5b1f17b72f	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > STREAM TERRACE	1
7150	6054	STREAM	1d2d0777-b47e-45ee-ac85-2d7b9f6e4ffd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > STREAM	1
7151	6054	SWAMP	4811065d-7aed-45e0-ac31-6417123be10e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > SWAMP	1
7152	6054	VALLEY	87b01c3a-f64f-4764-8cb8-c40ebcd5a989	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > VALLEY	1
7153	6054	WATERFALL	948dea97-9843-4895-b59b-cb55f07a41b4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > WATERFALL	1
7154	6054	WATERSHED/DRAINAGE BASINS	97a71326-75ac-422f-941e-c0c2897dd46b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > WATERSHED/DRAINAGE BASINS	1
7155	6055	ABRASION	efacd4f6-59ea-4019-8265-8cc81ecc99c0	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ABRASION	1
7156	6055	ATTRITION	9eedd20e-fce3-4fb2-9871-c0a327565ad9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ATTRITION	1
7157	6055	DEGRADATION	800606ea-9890-4475-af7b-100f529858d1	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > DEGRADATION	1
7158	6055	DOWNCUTTING	aff6bb19-84d0-40ed-8b81-a2210c468283	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > DOWNCUTTING	1
7159	6055	ENTRAINMENT	e89704aa-91a0-4888-bb33-a9073eff7119	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > ENTRAINMENT	1
7160	6055	HYDRAULIC ACTION	267eca20-09a7-46ad-89f4-111ccb3fd16d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > HYDRAULIC ACTION	1
7161	6055	LANDSLIDE	54e5d072-5a2c-471b-bca0-7e4ca32a2001	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > LANDSLIDE	1
7162	6055	SALTATION	93596daf-d2d3-4bb8-9626-9db100c402de	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SALTATION	1
7163	6055	SEDIMENT TRANSPORT	0c33b48d-1dd1-4309-bcd4-1ce3d0e24b46	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENT TRANSPORT	1
7164	6055	SEDIMENTATION	984e15c6-7eac-45b8-b098-ad82eab6be6e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION	1
7165	6055	SUSPENSION	8009663e-73c7-403e-b849-f40d2c3e3de8	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SUSPENSION	1
7166	6055	WEATHERING	6f47d087-21dc-41bc-955e-6eb2db8890cd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > WEATHERING	1
7167	6057	ARETES	8e73bff6-c2f9-46a6-963b-8ef09dd7f5f3	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ARETES	1
7168	6057	CIRQUES/COMBES	ae3b0c3d-35a1-4c94-ba72-ffe1a641902e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CIRQUES/COMBES	1
7169	6057	CREVASSES	e0d85cf0-b477-47df-a067-18e28a3e228f	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES	1
7170	6057	DRUMLINS	4be9b544-68fa-45ea-89f1-a44a9f5929e5	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > DRUMLINS	1
7171	6057	ESKERS	5e012809-98cf-468f-bdf7-7cea8569d3ab	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ESKERS	1
7172	6057	FJORDS	6aed82cb-be90-4e58-ae33-14943ea555be	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > FJORDS	1
7173	6057	GLACIAL HORNS	5477fad4-789b-436d-a01e-610aa8efa592	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIAL HORNS	1
7174	6057	GLACIER STRIATIONS/GROOVES	b2d3b8a4-4861-4c21-b875-97084b6e75aa	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER STRIATIONS/GROOVES	1
7175	6057	GLACIER/HANGING/U-SHAPED VALLEYS	d23f75ed-29ea-4aa2-8785-fd3a3726bc33	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER/HANGING/U-SHAPED VALLEYS	1
7176	6057	GLACIER/ICE CAVES	93b60653-f7bb-46f3-8f65-69221267018c	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > GLACIER/ICE CAVES	1
7177	6057	ICE-DAMMED LAKES	ee565a8c-72b9-44a4-b25d-efefd1a28d8d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ICE-DAMMED LAKES	1
7178	6057	KAME DELTA	3f86db44-f853-4eb3-b4e3-4aaee481043a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KAME DELTA	1
7179	6057	KAMES	89541868-0ea0-47c6-b81e-a0c4981f2d62	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KAMES	1
7180	6057	KETTLE HOLES	6d3722bb-29c0-4fb6-90c3-3f3a144b9941	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > KETTLE HOLES	1
7181	6057	MORAINES	4f590d94-110c-4762-9171-aba6d24af6a0	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES	1
7182	6057	NUNATAKS	3b8bdda1-2415-47ea-b4cf-c802fa44c496	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > NUNATAKS	1
7183	6057	OUTWASH FANS/PLAINS	a8bfc8ad-42f2-43cc-b161-20058037bb95	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > OUTWASH FANS/PLAINS	1
7184	6057	ROCHE MOUNTONNEES/SHEEPBACK	691cb42a-9de2-4f49-b1b4-9a4be80abd2b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ROCHE MOUNTONNEES/SHEEPBACK	1
7185	6057	ROCK GLACIERS	2d98cbaf-8c82-46e6-9962-a5e63918fe66	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > ROCK GLACIERS	1
7186	6057	TILL PLAINS	2bea72da-2cf3-403c-adb9-9d963eb71536	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > TILL PLAINS	1
7187	6058	ABLATION	99db4dca-4d07-48fd-8ba3-393532d04aa6	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ABLATION	1
7188	6058	ABRASION	8f57f4b0-5177-4362-81e8-ced75d37d1aa	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ABRASION	1
7189	6058	CRUST REBOUND	c06e70c0-616c-44f2-a884-ad0252e29e37	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > CRUST REBOUND	1
7190	6058	DEGRADATION	e60bfab8-01a8-4d0b-ae95-5d9014c71717	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > DEGRADATION	1
7191	6058	DUMPING	b6d56c3f-daa4-4c2f-9c56-4cecdf3d9fcd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > DUMPING	1
7192	6058	ENTRAINMENT	1dc7ed2f-2834-4044-8caa-117ce12389af	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > ENTRAINMENT	1
7193	6058	FIRN FORMATION	5b66d75f-331f-49d0-ad97-12f6535ce93a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FIRN FORMATION	1
7194	6058	FREEZE/THAW	f7849055-fa5c-437c-a8c6-08c7db3a3b0a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FREEZE/THAW	1
7195	6058	GLACIAL DISPLACEMENT	5ddbaf71-b279-42cf-b250-faaefb627f66	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL DISPLACEMENT	1
7196	6058	GLACIAL DRIFT	5cd3ad48-ade6-4306-a7de-4e68ecdf6bc7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL DRIFT	1
7197	6058	GLACIAL GROWTH	4be0198b-b88c-44db-b887-6cc7f5cd68f8	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL GROWTH	1
7198	6058	GLACIAL STRIATION	114e9f84-8bc5-4863-abd2-55b80ed2af11	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIAL STRIATION	1
7199	6058	GLACIER CRUST SUBSIDENCE	b87c5264-13c6-4716-acf3-51b2576dc1e9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > GLACIER CRUST SUBSIDENCE	1
7200	6058	PERIGLACIAL PROCESSES	fa0f38f3-2faa-4cd7-a848-22f3d96ab210	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > PERIGLACIAL PROCESSES	1
7201	6058	PLUCKING	c4619d3d-f852-4899-9e33-9fd6d4096351	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > PLUCKING	1
7202	6058	SCOURING	7ca88385-d0cf-439c-9a12-86b926b71582	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SCOURING	1
7203	6058	SEDIMENT TRANSPORT	791b7271-3a30-46ee-98e0-bc8239389950	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENT TRANSPORT	1
7204	6058	SEDIMENTATION	d8f33f0a-137c-49ac-aebf-f8a8b0540a09	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION	1
7205	6058	WEATHERING	580ef100-0fb8-456c-a9ca-565d11392a26	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > WEATHERING	1
7206	6059	CAVES	631c5fb8-5e44-48f8-b937-a5f393d0832d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > CAVES	1
7207	6059	COCKPIT/TOWER KARST	a20151df-e7cf-43e0-9745-ffc965f97ef7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > COCKPIT/TOWER KARST	1
7208	6059	KARST VALLEY	c319a44c-b21a-491f-9cf0-65868507576c	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > KARST VALLEY	1
7209	6059	SINKHOLES (DOLINES)	7f298307-73f6-4f10-96a2-db381f357cb6	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > SINKHOLES (DOLINES)	1
7210	6059	UVALA	40d9bf88-e7e2-4137-81fc-4721d67ce520	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST LANDFORMS > UVALA	1
7211	6060	CACO3	9902dc89-61fb-4a1e-becf-c8138122d2c4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > CACO3	1
7212	6060	DISSOLVED CO2	613abf26-7625-4134-8961-7a59fe82efc9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > DISSOLVED CO2	1
7213	6060	KARST HYDROLOGY	05172a3b-cdc0-4e97-af29-e38cd4f271c6	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > KARST HYDROLOGY	1
7214	6060	POROSITY	07f6c977-077b-47f2-962c-00dadcd9f555	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > POROSITY	1
7215	6060	WEATHERING	60dc0787-9e7e-4e0d-8023-d916da5d0836	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > WEATHERING	1
7216	6061	CALDERA	5d9d1d85-b402-4f84-ab5c-03a49fc68c25	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > CALDERA	1
7217	6061	CINDER CONE	7c394040-91f1-4438-a50a-3118254f5989	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > CINDER CONE	1
7218	6061	FAULTS	6107d1c4-5aea-4bfa-861d-d77083a4476e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > FAULTS	1
7219	6061	FOLDS	a2a3893c-de51-4ca7-a952-e9a43dd961a1	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > FOLDS	1
7220	6061	GEYSER	ea580c65-2f66-4745-bbb6-dde61279ecfa	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > GEYSER	1
7221	6061	GRABEN	524f075d-e875-4c9d-9e46-91f2a0b12168	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > GRABEN	1
7222	6061	HORST	bf3fbdaa-cefb-4a54-8a4e-ee0a862795fb	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > HORST	1
7223	6061	LAVA DOME	33a0cd6c-a8e4-4187-a2f3-7eb4bf62808d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > LAVA DOME	1
7224	6061	LAVA PLAIN	dc18db4d-2184-453e-ba0a-86c83a9bede0	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > LAVA PLAIN	1
7225	6061	MAAR	c1f717e9-da1a-4e85-ba2b-01986d53674d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > MAAR	1
7226	6061	MOUNTAINS	c34ea556-10bd-4665-9f22-68b5d05c9aea	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > MOUNTAINS	1
7227	6061	PLATEAU	0baf564f-f942-4aeb-9b75-30b838f28f3f	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > PLATEAU	1
7228	6061	RIDGE	ca091be1-4762-49ec-859b-a1a2fcb8e038	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > RIDGE	1
7229	6061	RIFT VALLEY	0bd4d492-4911-4a6a-afaa-34899a80294b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > RIFT VALLEY	1
7230	6061	TUYA	a355aafc-f0ce-4774-afc3-82b41df5f022	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > TUYA	1
7231	6061	VOLCANO	cefe2205-809c-4386-915e-a8737ae8e68e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC LANDFORMS > VOLCANO	1
7232	6062	EPEIROGENIC MOVEMENT	ebcd5f14-9468-493b-b0e6-de5afda2621a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > EPEIROGENIC MOVEMENT	1
7233	6062	ISOSTATIC UPLIFT	ca464924-4299-46ea-8cae-fd9bad49c1b1	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > ISOSTATIC UPLIFT	1
7234	6062	OROGENIC MOVEMENT	46d188a9-1099-4d72-b466-6e839297320e	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > OROGENIC MOVEMENT	1
7235	6062	RIFTING	9c207e15-9947-4849-bdf4-c1893a7f800a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > RIFTING	1
7236	6062	SUBDUCTION	44dd98d0-a0d0-46b2-bb98-ed887ce7fa60	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > SUBDUCTION	1
7237	6062	TECTONIC UPLIFT	4bc109b5-6788-4f64-8238-745bab3910dd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > TECTONIC PROCESSES > TECTONIC UPLIFT	1
7238	6063	ENERGY DISTRIBUTION	9d258088-e5bd-42b9-a281-e566da10ea74	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL ENERGY > ENERGY DISTRIBUTION	1
7239	6063	ENERGY OUTPUT	64461e23-b3c1-4b99-b879-84e54bacdb24	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL ENERGY > ENERGY OUTPUT	1
7240	6064	AMBIENT TEMPERATURE	1d2ac206-0977-4145-b334-baa6e13a0db6	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL TEMPERATURE > AMBIENT TEMPERATURE	1
7241	6064	TEMPERATURE GRADIENT	99d567bb-7767-4ea4-a135-a611eac6a669	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL TEMPERATURE > TEMPERATURE GRADIENT	1
7242	6064	TEMPERATURE PROFILES	321d9086-fc85-40a3-a2e0-d24bc6765345	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL TEMPERATURE > TEMPERATURE PROFILES	1
7243	6066	ISOSTATIC ADJUSTMENTS	5dee7d0e-e13e-4974-9750-79d5cd886c7a	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > CRUSTAL MOTION > ISOSTATIC ADJUSTMENTS	1
7244	6066	OCEAN CRUST DEFORMATION	aa6c2fe7-3261-4fd8-bed4-81403bc49086	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > CRUSTAL MOTION > OCEAN CRUST DEFORMATION	1
7245	6070	ANNUAL ELLIPTICAL COMPONENT	9d184041-9848-4f76-affd-74f4e4fd7462	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > POLAR MOTION > ANNUAL ELLIPTICAL COMPONENT	1
7246	6070	CHANDLER CIRCULAR COMPONENT	a983aad3-c72a-49e8-8de9-e0aaf35e14b3	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > POLAR MOTION > CHANDLER CIRCULAR COMPONENT	1
7247	6071	ROTATIONAL RATE/SPEED	d5d9bd6a-92c4-49ac-bddf-0077cf804ea7	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > ROTATIONAL MOTION/VARIATIONS > ROTATIONAL RATE/SPEED	1
7248	6071	TIDAL FRICTION	4bb526d7-2c14-43bc-a2a7-f166b5c41a3a	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > ROTATIONAL MOTION/VARIATIONS > TIDAL FRICTION	1
7249	6072	ANGLE OF ELEVATION	96427b44-91a8-4ace-8276-0117948878ee	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION > ANGLE OF ELEVATION	1
7250	6072	ANGLE OF INCLINATION	025d666e-a5bb-48b5-9890-129e60104611	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION > ANGLE OF INCLINATION	1
7251	6072	ORBIT TYPE	e709d2f9-c110-4e71-b4da-ff1a7c382d99	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION > ORBIT TYPE	1
7252	6072	ORBIT VELOCITY	53eeb68a-615d-42d0-9c6b-ddfe0d0eb2c7	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION > ORBIT VELOCITY	1
7253	6072	ORBITAL POSITION	e72ba365-ea43-42ef-acd1-05ac5c46f29a	EARTH SCIENCE > SOLID EARTH > GRAVITY/GRAVITATIONAL FIELD > SATELLITE ORBITS/REVOLUTION > ORBITAL POSITION	1
7254	6075	MAJOR ELEMENTS	2440389a-d0d9-445a-9dce-908900f0c3a7	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > ELEMENTS > MAJOR ELEMENTS	1
7255	6075	MINOR ELEMENTS	63cf1bca-72c7-4f5e-8018-3d22befa7147	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > ELEMENTS > MINOR ELEMENTS	1
7256	6075	RADIOACTIVE ELEMENTS	334f47c1-fd13-483f-b493-e69a9e93d553	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > ELEMENTS > RADIOACTIVE ELEMENTS	1
7257	6075	TRACE ELEMENTS	c3c898d7-14db-4536-bd86-f8f222167195	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > ELEMENTS > TRACE ELEMENTS	1
7258	6076	GAS HYDRATES AGE DETERMINATIONS	43561874-c5c4-47d5-8daf-e99fab694042	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES AGE DETERMINATIONS	1
7259	6076	GAS HYDRATES FORMATION	9589c9f5-fd13-4809-b26c-bd71db371836	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES FORMATION	1
7260	6076	GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES	1f76b928-d41a-4fbd-9da7-b8602f0183bd	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES	1
7261	6076	GAS HYDRATES VERTICAL/GEOGRAPHIC DISTRIBUTION	7a20b919-a6f6-453e-9055-a66a9da8594b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7262	6077	IGNEOUS ROCK AGE DETERMINATIONS	53e3eeca-265b-42d8-ad64-bfcc2acdad26	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK AGE DETERMINATIONS	1
7263	6077	IGNEOUS ROCK FORMATION	984d4966-070d-4f8c-85e7-83bb0fd804a8	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK FORMATION	1
7264	6077	IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES	a17a781d-01b0-470c-a4e2-e91ca8b1fbdc	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES	1
7265	6077	IGNEOUS ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	16499bb4-95bd-4bc0-b8d8-1fd11ca7d44d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7266	6078	METALS AGE DETERMINATIONS	a1b409b9-bf98-490a-8af5-f64fcda17a54	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS AGE DETERMINATIONS	1
7267	6078	METALS PHYSICAL/OPTICAL PROPERTIES	85d46af8-f6ce-490d-a971-0f03b301c1e4	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES	1
7268	6078	METALS VERTICAL/GEOGRAPHIC DISTRIBUTION	fbc418a0-5d32-43ab-9f1f-e81b9d8534e1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7269	6079	METAMORPHIC ROCK AGE DETERMINATIONS	02a53a61-4fd2-4294-9dcc-071f701bc263	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK AGE DETERMINATIONS	1
7270	6079	METAMORPHIC ROCK FORMATION	a243624b-a9c8-4c53-84d1-bb0fe2a71ef6	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK FORMATION	1
7271	6079	METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES	2d38e7c6-8169-49e9-ab9d-0d0f690cce04	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES	1
7272	6079	METAMORPHIC ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	5d80d2d2-7841-4734-a8c5-5d60679e3830	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7273	6080	METEORITE AGE DETERMINATIONS	6d75d735-7dac-42a2-8f87-2dfcbe3cf545	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE AGE DETERMINATIONS	1
7274	6080	METEORITE ORIGIN	d45ccf89-7f8c-4a61-b46d-c34dca21c879	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE ORIGIN	1
7275	6080	METEORITE PHYSICAL/OPTICAL PROPERTIES	3ff47a50-2f58-489b-96a7-74e1d40cf0f2	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES	1
7276	6080	METEORITE VERTICAL/GEOGRPAHIC DISTRIBUTION	e468e55a-5bee-413e-8cbd-c9706e28eb93	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE VERTICAL/GEOGRPAHIC DISTRIBUTION	1
7277	6082	MINERAL AGE DETERMINATIONS	239c04ba-6f82-4d4f-a60b-a1ee49301e0f	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL AGE DETERMINATIONS	1
7278	6082	MINERAL FORMATION	f6ce9d55-4183-4433-a615-4c4f01d7810b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL FORMATION	1
7279	6082	MINERAL PHYSICAL/OPTICAL PROPERTIES	da269095-7270-4a0d-8b43-2c85bd42dd90	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES	1
7280	6082	MINERAL VERTICAL/GEOGRAPHIC DISTRIBUTION	cbac3817-116f-4280-b32d-d30bb0f37cbd	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7281	6082	MINERALOIDS	56373f39-7c27-4a77-bb52-c4defee751f8	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERALOIDS	1
7282	6083	NON-METALLIC MINERAL AGE DETERMINATIONS	497ec0b6-a732-4d97-9e5a-09eaf5ed4607	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL AGE DETERMINATIONS	1
7283	6083	NON-METALLIC MINERAL FORMATION	2b4d3c45-8713-4ec9-9565-866bb01be9f9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL FORMATION	1
7284	6083	NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES	42424cb5-aa02-4e7e-b164-b2a3324285c6	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES	1
7285	6083	NON-METALLIC MINERAL VERTICAL/GEOGRAPHIC DISTRIBUTION	1980c6c6-50f0-45a1-9a28-668f1372c09e	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7286	6084	COAL	8b726747-6eba-4ce6-bfc6-ee84616a1862	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > COAL	1
7287	6084	SEDIMENTARY ROCK AGE DETERMINATIONS	701f2b6f-34b0-4f69-941e-c2c5545abc0b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK AGE DETERMINATIONS	1
7288	6084	SEDIMENTARY ROCK FORMATION	8777e995-2acc-40cd-b81a-f0c7b69df23e	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK FORMATION	1
7289	6084	SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES	609aeae6-388f-41a1-8813-a2e760e8fdb7	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES	1
7290	6084	SEDIMENTARY ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	23706ac6-8f15-4548-b1c5-6594d825d56d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK VERTICAL/GEOGRAPHIC DISTRIBUTION	1
7291	6056	EARTHQUAKE MAGNITUDE/INTENSITY	4bc185d3-e2c5-4acc-bce8-37fea7d8fc0b	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > EARTHQUAKE MAGNITUDE/INTENSITY	1
7292	6056	EARTHQUAKE OCCURRENCES	752d4f80-a418-4a75-a9eb-772222af1746	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > EARTHQUAKE OCCURRENCES	1
7293	6056	EARTHQUAKE PREDICTIONS	131c1e46-efca-4478-a5d1-d7193483bb96	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > EARTHQUAKE PREDICTIONS	1
7294	6056	SEISMIC PROFILE	688191e0-c70c-4cf9-a5b6-a26a2bca7198	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > SEISMIC PROFILE	1
7297	6087	FOLDS	a71c3d9d-7144-4107-add5-0aed0c731dbc	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > FOLDS	1
7298	6087	ISOSTATIC REBOUND	5e7a091a-894f-423f-a431-ab52cf205311	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > ISOSTATIC REBOUND	1
7299	6087	LITHOSPHERIC PLATE MOTION	64ccd7be-577b-4784-8072-8c456aab2185	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > LITHOSPHERIC PLATE MOTION	1
7300	6087	PLATE BOUNDARIES	4adc15b8-0c18-4ccd-a6ec-75be82df5359	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > PLATE BOUNDARIES	1
7301	6087	STRAIN	5d7f7568-bfc3-4c11-b446-c4f6488c8ae9	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > STRAIN	1
7302	6087	STRATIGRAPHIC SEQUENCE	efe175a0-100b-404b-a702-2e179bee034a	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > STRATIGRAPHIC SEQUENCE	1
7303	6087	STRESS	29dbe37e-22e6-4d02-844f-60359fbbc130	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > STRESS	1
7304	6088	ERUPTION DYNAMICS	0db0e1c8-6ba3-40c4-97c2-d78c9812692b	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS	1
7305	6088	VOLCANO MAGNITUDE/INTENSITY	14e0d39a-ff1c-46d9-b162-481f80beac91	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > VOLCANO MAGNITUDE/INTENSITY	1
7306	6088	VOLCANO OCCURRENCES	d1ab518b-0152-48cf-a9c6-47c5920ed773	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > VOLCANO OCCURRENCES	1
7307	6088	VOLCANO PREDICTIONS	3adb9c52-df47-4390-a682-56e1774e8cdb	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > VOLCANO PREDICTIONS	1
7308	6181	SNOW GRAIN SIZE	2ba27dc1-e2e6-4ce5-be05-fb4e4dd5ab54	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GLACIERS/ICE SHEETS > FIRN > SNOW GRAIN SIZE	1
7309	6191	AQUIFERS	a957363b-2f2c-4169-a656-c2f24933eb72	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER FEATURES > AQUIFERS	1
7310	6191	FRESHWATER SPRINGS	c87c086a-933f-44c7-a128-33279b36d7b5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER FEATURES > FRESHWATER SPRINGS	1
7311	6191	WATER TABLE	ecbe9f17-6012-4e39-a707-713973b7d167	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER FEATURES > WATER TABLE	1
7312	6192	AQUIFER RECHARGE	dbeaaf9f-294c-4e45-ba9e-7be8cd449db1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE	1
7313	6192	DISCHARGE	0976b778-91be-40e7-9ed7-ebbf214bb818	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISCHARGE	1
7314	6192	DISPERSION	d2d4ee50-99ed-4ee7-b957-22271a60c031	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISPERSION	1
7315	6192	DRAINAGE	6a2107ab-38ab-42dc-beb0-8ba5f65e8022	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DRAINAGE	1
7316	6192	INFILTRATION	638a22af-4e97-450e-a278-b81338443230	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > INFILTRATION	1
7317	6192	LAND SUBSIDENCE	a1bf1e84-c4e7-4154-ad0a-4b9eedf45066	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > LAND SUBSIDENCE	1
7318	6192	PERCOLATION	d64094ae-774b-4435-8f2e-a54d114e5555	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > PERCOLATION	1
7319	6192	SALTWATER INTRUSION	4a11a257-99c6-4f87-8884-2a2aa46a49fa	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SALTWATER INTRUSION	1
7320	6192	SUBSURFACE FLOW	872a0464-884c-4d6f-8f06-0679329dadcc	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SUBSURFACE FLOW	1
7321	6219	DRAINAGE BASINS	272700c5-d762-452b-8e9f-130e3a51efb5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES > DRAINAGE BASINS	1
7322	6219	LAKES/RESERVOIRS	3d64f625-fb84-4178-ad08-4be2dd15979b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES > LAKES/RESERVOIRS	1
7323	6219	RIVERS/STREAMS	5e3c573f-a787-4afa-80a4-047c2c5d83f2	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES > RIVERS/STREAMS	1
7324	6219	WATER CHANNELS	4b276110-57bc-4ed6-b741-1ec0383fa962	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES > WATER CHANNELS	1
7325	6219	WETLANDS	d138302a-03b3-4cf7-95db-ac98f863c04f	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER FEATURES > WETLANDS	1
7326	6220	AQUIFER RECHARGE	3609b843-d840-460c-b1a3-d4fcc69a32f6	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE	1
7327	6220	DISCHARGE/FLOW	36a2999b-2255-4d4e-a249-40df3b7b3aaf	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DISCHARGE/FLOW	1
7328	6220	DRAINAGE	269c7277-fa8f-4c1c-bd8b-ab772c1df4e5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DRAINAGE	1
7329	6220	FLOODS	7fdc339e-017f-4e4b-89a3-12e441a40bad	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > FLOODS	1
7330	6220	HYDROPATTERN	960037c5-57b1-4cdf-84be-4542beee7d5a	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > HYDROPATTERN	1
7331	6220	HYDROPERIOD	d4e8b5c5-9203-4982-82bc-2611b517ffdb	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > HYDROPERIOD	1
7332	6220	INUNDATION	c6c0c5dd-c0ca-4670-bbaa-c22d39e73570	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > INUNDATION	1
7333	6220	RUNOFF	f6a54329-486b-4d5f-b105-c639cec42351	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > RUNOFF	1
7334	6220	STAGE HEIGHT	5cb5d5b9-0c0b-497f-a4ea-a8cece52d13d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > STAGE HEIGHT	1
7335	6220	TOTAL SURFACE WATER	6f52de55-f5f2-45c0-b83f-59dbfb1fe221	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > TOTAL SURFACE WATER	1
7336	6220	WATER DEPTH	42aa1fa1-56a9-4e96-8063-077bd7ba88d8	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > WATER DEPTH	1
7337	6220	WATER PRESSURE	84784fef-5b76-45a0-91e0-28788e09fea6	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > WATER PRESSURE	1
7338	6220	WATER YIELD	04922ba6-8f00-4f54-b80c-ce2414c91e2e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > WATER YIELD	1
7339	6221	WATERSHED BOUNDARIES	b98123fc-6a87-4396-8e1a-ae7406e76ff6	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS > WATERSHED BOUNDARIES	1
7340	6221	WATERSHED DRAINAGE	ae36ad48-85f2-42a0-958f-efec71c34cc0	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS > WATERSHED DRAINAGE	1
7341	6221	WATERSHED LENGTH	e12150d7-5bd3-4a22-8b9f-f887a1fe3096	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS > WATERSHED LENGTH	1
7342	6221	WATERSHED SHAPE	2b37d67c-92a6-4188-8f1b-4462bd754577	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS > WATERSHED SHAPE	1
7343	6221	WATERSHED SLOPE	0d209f3c-73b1-412d-828b-22b25da8fc3a	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > WATERSHED CHARACTERISTICS > WATERSHED SLOPE	1
7344	6222	ACID RAIN	62ee81e7-9f5a-4af5-a086-f4c402c7d19d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > ACID RAIN	1
7345	6222	ARSENIC	fa892a9e-523b-424e-bf02-1a8d1e618985	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > ARSENIC	1
7346	6222	BARIUM	3e666b9f-6cf5-4454-9a65-987e981cd80e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > BARIUM	1
7347	6222	CALCIUM	e5a658d5-74db-4022-894f-edc8d297767a	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > CALCIUM	1
7348	6222	CARCINOGENS	31c913e1-9692-45b5-bce5-cca46fa1874d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > CARCINOGENS	1
7349	6222	CHROMIUM	9ab53717-17f1-4259-b425-0eed19c31884	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > CHROMIUM	1
7350	6222	COPPER	78fb5691-136d-40f8-a834-6e6f4cd768ff	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > COPPER	1
7351	6222	DISINFECTANTS	4690d6a8-78cd-48bc-82f5-36fb16d4c52e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > DISINFECTANTS	1
7352	6222	HARMFUL ALGAL BLOOMS (HABs)	1b6e67ff-351f-490c-bb43-646ac71f52ea	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > HARMFUL ALGAL BLOOMS (HABs)	1
7353	6222	INORGANIC MATTER	e848dbd1-b70a-4820-a630-98bd642ae357	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > INORGANIC MATTER	1
7354	6222	IRON	0965eb7b-6bd3-48a3-aa2a-52d7e2dda8ad	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > IRON	1
7355	6222	LEAD	6fe420c1-2285-4031-babe-f0243c59a617	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > LEAD	1
7356	6222	MAGNESIUM	38f99d8b-80af-439a-9d3f-1e72aef5d7c3	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > MAGNESIUM	1
7357	6222	METALS/MINERALS	961591ce-9207-47db-9aeb-11586371fa12	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > METALS/MINERALS	1
7358	6222	ORGANIC MATTER	9c90825c-a35f-4165-8248-e90ab869f8ec	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > ORGANIC MATTER	1
7359	6222	PATHOGEN	6fff6994-a0d8-4f19-8d36-c9f354b08b19	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > PATHOGEN	1
7360	6222	PESTICIDES	bc1c6d8c-2e47-4a9f-aeb4-16b02bff4f19	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > PESTICIDES	1
7361	6222	PETROLEUM HYDROCARBONS	aef23021-81c1-4540-a0a5-35c590142a6d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > PETROLEUM HYDROCARBONS	1
7362	6222	POTASSIUM	072721be-eb8b-4ac4-9354-251dbf74ade0	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > POTASSIUM	1
7363	6222	SELENIUM	b2318fb3-788c-4f36-a1d1-36670d2da747	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > SELENIUM	1
7364	6222	SEWAGE OVERFLOWS	207da091-2cd5-49a7-950e-91a164e02637	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > SEWAGE OVERFLOWS	1
7365	6222	TITANIUM	160cce6b-c9f5-45bf-9a51-ee477f446cce	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > TITANIUM	1
7366	6222	TOXIC CHEMICALS	bf3aaf41-3502-49cf-89df-4613ce87c9c3	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > TOXIC CHEMICALS	1
7367	6222	TRACE METALS	f2d6aa01-5070-4147-bae1-4b2cad2c3987	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > TRACE METALS	1
7368	6222	ZINC	ab12b3d6-2cbf-4a5a-a410-1d23afe906d8	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > CONTAMINANTS > ZINC	1
7369	6223	DISSOLVED CARBON DIOXIDE	a9b89557-c09f-4a4a-a1eb-47c632f8eb59	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > GASES > DISSOLVED CARBON DIOXIDE	1
7370	6223	DISSOLVED GASES	ac933400-3c8c-4db4-ac68-5e8ed06c8336	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > GASES > DISSOLVED GASES	1
7371	6223	DISSOLVED NITROGEN	dc748b93-e7d6-419d-a9f0-f370556d6f8e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > GASES > DISSOLVED NITROGEN	1
7372	6223	DISSOLVED OXYGEN	b632d0cc-d4b0-458e-a182-16bbd2a5ab05	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > GASES > DISSOLVED OXYGEN	1
7373	6224	RADIOISOTOPES	6f4e850f-84e4-466f-b5ad-2032ea2187ea	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > ISOTOPES > RADIOISOTOPES	1
7374	6224	STABLE ISOTOPES	fb52b51d-8bb4-4b04-907b-c130ec706f85	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > ISOTOPES > STABLE ISOTOPES	1
7375	6225	HYDROCARBONS	0ba2ccb3-332c-4ee6-a9c9-50dce5a6c0cc	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > HYDROCARBONS	1
7376	6225	INORGANIC MATTER	9bdac7db-be34-4eed-91bc-28f6628ed044	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > INORGANIC MATTER	1
7377	6225	NITROGEN COMPOUNDS	644e0f53-98a2-4512-a228-00f5e61fd93d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > NITROGEN COMPOUNDS	1
7378	6225	NITROGEN	bf03dba8-2881-44ac-abfc-ba3353f67a24	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > NITROGEN	1
7379	6225	ORGANIC MATTER	ee92daf8-d0da-4476-b389-0485114cbbe9	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > ORGANIC MATTER	1
7380	6225	PHOSPHOROUS	846d2db9-41cd-4ae8-b4ff-a34a9efb7428	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > NUTRIENTS > PHOSPHOROUS	1
7381	6226	SEDIMENTS	6d2511f8-4503-4237-93a9-34a3b369fe00	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > SOLIDS > SEDIMENTS	1
7610	6638	COLD SEEP	290354cc-c670-4845-bb66-ef1974b1e2a2	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ABYSSAL > COLD SEEP	1
7382	6226	SUSPENDED SOLIDS	9d8cb1dd-4b38-4b4e-8532-ab4eb72cd4ae	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > SOLIDS > SUSPENDED SOLIDS	1
7383	6226	TOTAL DISSOLVED SOLIDS	7d82a1f7-aa6e-47c7-8eb3-78bfe2e4349b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > SOLIDS > TOTAL DISSOLVED SOLIDS	1
7384	6227	ALKALINITY	a74059fe-6b15-4b55-8ea5-4a65b66c7e11	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > ALKALINITY	1
7385	6227	BIOCHEMICAL OXYGEN DEMAND (BOD)	2ef34dc5-4d29-4820-963c-f830f46c0347	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > BIOCHEMICAL OXYGEN DEMAND (BOD)	1
7386	6227	CHLOROPHYLL CONCENTRATIONS	de21632f-b614-4375-8f09-d14ab00d852b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > CHLOROPHYLL CONCENTRATIONS	1
7387	6227	CONDUCTIVITY	d14389d9-54f5-41a0-b8e8-dc9d8f87e4e2	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > CONDUCTIVITY	1
7388	6227	EUTROPHICATION	53d36c39-3cb1-44db-9746-feee86cbe9d7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > EUTROPHICATION	1
7389	6227	HYDROCARBONS	344cbd30-a2e4-437e-9fc9-5e6b1c484bac	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > HYDROCARBONS	1
7390	6227	INORGANIC MATTER	6cf87a79-e8b0-4ff1-9039-f3ad1f1f17a7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > INORGANIC MATTER	1
7391	6227	LIGHT TRANSMISSION	45351e81-fcd4-46a1-9222-315946caefc7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > LIGHT TRANSMISSION	1
7392	6227	NITROGEN COMPOUNDS	1886b524-1f51-447d-9805-d40859739a0e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > NITROGEN COMPOUNDS	1
7393	6227	ORGANIC MATTER	e82c0632-5a3c-4da2-ba10-55c0fc222580	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > ORGANIC MATTER	1
7394	6227	PHOSPHOROUS COMPOUNDS	f9f5cedd-9a0e-4058-87ff-c97df63fc326	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > PHOSPHOROUS COMPOUNDS	1
7395	6227	POTABILITY	dac96944-5a5e-4b2a-802d-74627bb93db9	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > POTABILITY	1
7396	6227	SALINE CONCENTRATION	a38db528-3064-449d-ae70-af86997a11f4	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > SALINE CONCENTRATION	1
7397	6227	TURBIDITY	0eaf009f-f92b-48b5-8a71-9c44c80d03d4	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > TURBIDITY	1
7398	6227	WATER COLOR	e8d6a9c3-864e-4d97-938f-a6203997c01f	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER COLOR	1
7399	6227	WATER HARDNESS	75a83951-a086-4d25-9ab0-c118b0e20383	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER HARDNESS	1
7400	6227	WATER ION CONCENTRATIONS	4cc8def9-a825-4ede-9e34-4e11cf89488d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER ION CONCENTRATIONS	1
7401	6227	WATER ODOR	d05ac6d6-d397-4bf7-b62b-c270522de2a5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER ODOR	1
7402	6227	WATER TEMPERATURE	61594015-4ab4-4b38-ae4f-e31a4757b065	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER TEMPERATURE	1
7403	6227	WATER TRACE ELEMENTS	475c95a4-fd1c-4015-825f-07f6529858b0	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > WATER TRACE ELEMENTS	1
7404	6227	pH	14625f2a-4186-4377-a0d9-88998bb6b775	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER CHARACTERISTICS > pH	1
7405	6228	GLOBAL DRINKING WATER QUALITY INDEX	a71d195e-ff30-4592-a22c-a82af92f3d1f	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER QUALITY INDEXES > GLOBAL DRINKING WATER QUALITY INDEX	1
7406	6228	INDEX OF BIOTIC INTEGRITY	4497eb1b-b64d-46ff-a18d-37d217430777	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER QUALITY INDEXES > INDEX OF BIOTIC INTEGRITY	1
7407	6228	NATIONAL SANITATION FOUNDATION WATER QUALITY INDEX	989e0558-a5fb-4758-bb82-c7d0a6a9f319	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER QUALITY INDEXES > NATIONAL SANITATION FOUNDATION WATER QUALITY INDEX	1
7408	6228	TROPHIC STATE INDEX	4fbe9a29-e3f5-4e1f-9dcb-99b79485d3b2	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > WATER QUALITY/WATER CHEMISTRY > WATER QUALITY INDEXES > TROPHIC STATE INDEX	1
7409	6293	DEWPOINT DEPRESSION	a5e36040-cc5e-46d1-aeee-f49902e943b2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > DEW POINT TEMPERATURE > DEWPOINT DEPRESSION	1
7410	6294	24 HOUR MAXIMUM TEMPERATURE	ce6a6b3a-df4f-4bd7-a931-7ee874ee9efe	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > MAXIMUM/MINIMUM TEMPERATURE > 24 HOUR MAXIMUM TEMPERATURE	1
7411	6294	24 HOUR MINIMUM TEMPERATURE	5c7f35d5-a3ec-4010-b1c3-6e98ac29dc3f	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > MAXIMUM/MINIMUM TEMPERATURE > 24 HOUR MINIMUM TEMPERATURE	1
7412	6294	6 HOUR MAXIMUM TEMPERATURE	e56bcf72-f331-4545-948f-73fe0193b1bd	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > MAXIMUM/MINIMUM TEMPERATURE > 6 HOUR MAXIMUM TEMPERATURE	1
7413	6294	6 HOUR MINIMUM TEMPERATURE	c9ab66f1-91c6-497a-b8d6-4688160b0e16	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > SURFACE TEMPERATURE > MAXIMUM/MINIMUM TEMPERATURE > 6 HOUR MINIMUM TEMPERATURE	1
7414	6303	DEW POINT DEPRESSION	86fb8a31-35f6-4d0e-b4b4-f9cecf961a47	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > DEW POINT TEMPERATURE > DEW POINT DEPRESSION	1
7415	6305	DRY ADIABATIC LAPSE RATE	17ce714a-bd7e-41a2-ab3d-4865832f1f0a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VERTICAL PROFILES > DRY ADIABATIC LAPSE RATE	1
7416	6305	ENVIRONMENTAL LAPSE RATE	050771bb-27a3-4e47-bd1b-724d1d73e20c	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VERTICAL PROFILES > ENVIRONMENTAL LAPSE RATE	1
7417	6305	INVERSION HEIGHT	4fa883a3-e312-4dbe-870e-3272de4ac76a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VERTICAL PROFILES > INVERSION HEIGHT	1
7418	6305	SATURATED ADIABATIC LAPSE RATE	65937e73-0cc0-4058-b7dc-12c418ba2ed5	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC TEMPERATURE > UPPER AIR TEMPERATURE > VERTICAL PROFILES > SATURATED ADIABATIC LAPSE RATE	1
7419	6308	ABSOLUTE HUMIDITY	6b61a904-b92d-45ee-9061-aa5e61c29dd2	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > ABSOLUTE HUMIDITY	1
7420	6308	HUMIDITY MIXING RATIO	ea308986-ad35-4482-948c-5eb1a01be836	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > HUMIDITY MIXING RATIO	1
7421	6308	RELATIVE HUMIDITY	a249c68f-8249-4285-aad2-020b3c5aefc3	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > RELATIVE HUMIDITY	1
7422	6308	SATURATION SPECIFIC HUMIDITY	ba2491a4-2498-4c9f-9adc-123078eef633	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > SATURATION SPECIFIC HUMIDITY	1
7423	6308	SPECIFIC HUMIDITY	811391d2-4113-4d52-9c88-47d56afda481	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR INDICATORS > HUMIDITY > SPECIFIC HUMIDITY	1
7424	6319	EFFECTIVE EVAPOTRANSPIRATION	f28060e0-1c51-41df-8451-6c98b3e77e8a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > EVAPOTRANSPIRATION > EFFECTIVE EVAPOTRANSPIRATION	1
7425	6319	POTENTIAL EVAPOTRANSPIRATION	6045993e-a656-40c1-853c-9db1fbb49171	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WATER VAPOR > WATER VAPOR PROCESSES > EVAPOTRANSPIRATION > POTENTIAL EVAPOTRANSPIRATION	1
7426	6332	ANABATIC WINDS	5f55961d-45b8-4330-8eee-0b9a9eb4f309	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > ANABATIC WINDS	1
7427	6332	BORA WINDS	2cf573dd-0ed7-4455-a233-5987b5a8b52a	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > BORA WINDS	1
7428	6332	FOEHN WINDS	c19501d9-bd86-4611-bd30-6a34dc763a35	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > FOEHN WINDS	1
7429	6332	KATABATIC WINDS	d7d48399-62ac-4eca-9c09-14b9094a9444	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > KATABATIC WINDS	1
7430	6332	MOUNTAIN BREEZES	6520897f-c6b6-432e-b7d5-e99b33e6932e	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > MOUNTAIN BREEZES	1
7431	6332	VALLEY BREEZES	4d005bfc-597b-4a99-971f-21d3d44b7b91	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > LOCAL WINDS > OROGRAPHIC WINDS > VALLEY BREEZES	1
7432	6357	POTENTIAL VORTICITY	72edbeca-b608-4f2d-8aba-492c8e6615b8	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > VORTICITY > POTENTIAL VORTICITY	1
7433	6357	VORTICITY ADVECTION	9e2f502b-a2d5-4bc8-8c8f-489aa0c68177	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > VORTICITY > VORTICITY ADVECTION	1
7434	6358	HORIZONTAL WIND SHEAR	ef91f2b6-27e9-42ab-b8c6-4410aace0141	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > WIND SHEAR > HORIZONTAL WIND SHEAR	1
7435	6358	VERTICAL WIND SHEAR	1b0abf68-b069-4a0b-8081-35a36da9d4a7	EARTH SCIENCE > ATMOSPHERE > ATMOSPHERIC WINDS > WIND DYNAMICS > WIND SHEAR > VERTICAL WIND SHEAR	1
7436	6367	DOWNWARD MOISTURE FLUX	1dc6063b-892d-4879-8551-1e346dd3f2e7	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > MOISTURE FLUX > DOWNWARD MOISTURE FLUX	1
7437	6367	UPWARD MOISTURE FLUX	49cad94d-0e93-44cb-a8a2-8e83d603463b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > MOISTURE FLUX > UPWARD MOISTURE FLUX	1
7438	6371	KARMAN VORTEX STREET	2d00d3c4-2ef3-49f6-9261-6184f6517b4f	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD DYNAMICS > VORTEX STREET > KARMAN VORTEX STREET	1
7439	6380	ACCRETION	ab702934-0959-45fc-a523-81e1aa0c09c8	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > DROPLET GROWTH > ACCRETION	1
7440	6380	AGGREGATION	8e484ec4-50fd-4c08-9c96-6ad483e170ad	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > DROPLET GROWTH > AGGREGATION	1
7441	6380	COALESCENCE	d5d64790-db29-451d-b022-a461dac06228	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > DROPLET GROWTH > COALESCENCE	1
7442	6382	SEDIMENTATION RATE	bee9f657-c115-4d73-a10c-7e05e00db574	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > SEDIMENTATION > SEDIMENTATION RATE	1
7443	6404	CUMULONIMBUS CALVUS	e1035388-6993-4143-966b-30ced627c2da	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULONIMBUS > CUMULONIMBUS CALVUS	1
7444	6404	CUMULONIMBUS CAPILLATUS	eec3cec2-1649-4507-b91d-3a25ab2200ee	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULONIMBUS > CUMULONIMBUS CAPILLATUS	1
7445	6404	PYROCUMULONIMBUS	772d8044-f11b-4b01-bc72-d7dd45cfe1b3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULONIMBUS > PYROCUMULONIMBUS	1
7446	6405	CUMULUS CASTELLANUS	29d6cd82-4762-4316-9fdd-29430dae7ad9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS CASTELLANUS	1
7447	6405	CUMULUS CONGESTUS	3bafe2e0-c1a7-4bee-a02e-ac66964b4d7f	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS CONGESTUS	1
7448	6405	CUMULUS HUMILIS	6aa7422c-ad66-40b6-90cd-750f9158daee	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS HUMILIS	1
7449	6405	CUMULUS MEDIOCRIS	ba9a8dac-abb7-4580-938d-762b53bab71b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS MEDIOCRIS	1
7450	6405	PYROCUMULUS	801846d5-622b-4937-83cf-9d387be73ac4	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > PYROCUMULUS	1
7451	6417	CIRRUS CLOUD SYSTEMS	e4f5faaa-36d9-4529-b667-7d4e39d3c67b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CIRRUS/SYSTEMS > CIRRUS CLOUD SYSTEMS	1
7452	6417	CIRRUS KELVIN-HELMHOLTZ COLOMBIAH	d6ba91a1-a5f4-47e3-9485-89348235acb9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/HIGH-LEVEL CLOUDS (OBSERVED/ANALYZED) > CIRRUS/SYSTEMS > CIRRUS KELVIN-HELMHOLTZ COLOMBIAH	1
7453	6420	ADVECTION FOG	30c9e32c-7dfe-430f-bd06-4cfa844076e2	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > ADVECTION FOG	1
7454	6420	FRONTAL FOG	09a1b23e-bd8b-4bb9-966b-2388328973d4	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > FRONTAL FOG	1
7455	6420	ICE FOG	cd4f6e31-14b5-468a-a15c-5ac0ce97bf35	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > ICE FOG	1
7456	6420	RADIATION FOG	99a0a2d2-5d77-4cf2-8fc0-90d12840b12d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > RADIATION FOG	1
7457	6420	STEAM FOG	50604404-fef4-4e17-a6a6-a88c0bd88c4f	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > STEAM FOG	1
7458	6420	UPSLOPE FOG	3eefb892-0453-48b6-b619-b8fa3e7bbfc8	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > FOG > UPSLOPE FOG	1
7459	6422	MARINE STRATOCUMULUS	b1d51b72-97d0-484c-b251-220f219965c2	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > MARINE STRATOCUMULUS	1
7460	6422	STRATOCUMULUS CUMILIFORMIS	5857260b-1de6-47c2-8f66-5c0dbac42e32	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS CUMILIFORMIS	1
7461	6422	STRATOCUMULUS UNDULATAS	bec5166e-1822-40f7-8f07-4d5167d8a565	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS UNDULATAS	1
7462	6424	ALTOCUMULUS CASTELLANUS	44415a90-bfe0-447a-93c9-6e4badc6871c	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOCUMULUS > ALTOCUMULUS CASTELLANUS	1
7463	6424	ALTOCUMULUS LENTICULARIS	dbc7fed3-ad30-4e57-868e-bae478713a71	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOCUMULUS > ALTOCUMULUS LENTICULARIS	1
7464	6424	ALTOCUMULUS UNDULATUS	73e102fa-3089-42c3-bd0f-4682f73fff0f	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOCUMULUS > ALTOCUMULUS UNDULATUS	1
7465	6425	ALTOSTRATUS UNDULATUS	4da38a31-aac6-4080-96b0-c8ee2cb33158	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOSTRATUS > ALTOSTRATUS UNDULATUS	1
7466	6430	FREEZING DRIZZLE	88e39edc-bf9b-4c02-8a9d-83f9b6c01891	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > DRIZZLE > FREEZING DRIZZLE	1
7467	6432	ACID RAIN	f9405e92-0c1c-4443-9cc4-45d662d8b5f2	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > RAIN > ACID RAIN	1
7468	6432	FREEZING RAIN	a90306f0-353c-4083-941a-0973a6fd6584	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > LIQUID PRECIPITATION > RAIN > FREEZING RAIN	1
7469	6442	SLEET	5beaf99c-0675-4af3-9236-f55d8d206d85	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > ICE PELLETS > SLEET	1
7470	6442	SMALL HAIL	26087764-bd76-4a70-8dba-3c0cbadad6a7	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > ICE PELLETS > SMALL HAIL	1
7471	6443	SNOW GRAINS	6a16461a-49b9-4887-802f-2320c6dc4dd2	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > SNOW > SNOW GRAINS	1
7472	6443	SNOW PELLETS	c2815464-48b7-4dc1-90d6-0ab5a8b7c82b	EARTH SCIENCE > ATMOSPHERE > PRECIPITATION > SOLID PRECIPITATION > SNOW > SNOW PELLETS	1
7473	6457	SUBTROPICAL DEPRESSION TRACK	241d4bbb-3965-4595-93d3-8fe8c89fdab1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES > SUBTROPICAL DEPRESSION > SUBTROPICAL DEPRESSION TRACK	1
7474	6458	SUBTROPICAL STORM MOTION	308beca2-b3c8-4cbb-aa9c-e1be605ca785	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES > SUBTROPICAL STORM > SUBTROPICAL STORM MOTION	1
7475	6458	SUBTROPICAL STORM TRACK	c1a196a3-4134-473a-819e-369ab9656abb	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > SUBTROPICAL CYCLONES > SUBTROPICAL STORM > SUBTROPICAL STORM TRACK	1
7476	6474	CYCLONES (SW INDIAN)	7067a3f8-2903-46b7-9189-af1189a15a43	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY > CYCLONES (SW INDIAN)	1
7477	6474	HURRICANES  (N. ATLANTIC/E. PACIFIC)	fb890034-3ae6-4c91-941c-ae1483a13528	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7478	6474	SEVERE CYCLONIC STORMS (N. INDIAN)	5da932fa-2f4b-4f65-bad4-18c661816549	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7479	6474	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	e89e331c-ca8e-4c25-be34-c81017bd019f	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7480	6474	TYPHOONS (WESTERN N. PACIFIC)	074c2800-e458-4fa0-bcae-7f400d970650	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > ACCUMULATED CYCLONE ENERGY > TYPHOONS (WESTERN N. PACIFIC)	1
7481	6475	CYCLONES (SW INDIAN)	0d7ea0fa-987a-4429-85e7-754ca638e504	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY > CYCLONES (SW INDIAN)	1
7482	6475	HURRICANES  (N. ATLANTIC/E. PACIFIC)	4354779d-94e6-4c38-973b-3a9bafa4eeb2	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7483	6475	SEVERE CYCLONIC STORMS (N. INDIAN)	7aa4aea2-0f5b-4490-967b-7e339eaec507	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7484	6475	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	ab9dfb44-979e-495c-ad83-8d30a37018be	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7485	6475	TYPHOONS (WESTERN N. PACIFIC)	dd5cbcc2-622a-4c3c-82b8-7e2869f8438a	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > LANDFALL INTENSITY > TYPHOONS (WESTERN N. PACIFIC)	1
7486	6476	CYCLONES (SW INDIAN)	1ab5b26c-8560-412c-8b7b-80921aff9fe1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND > CYCLONES (SW INDIAN)	1
7487	6476	HURRICANES  (N. ATLANTIC/E. PACIFIC)	93f7b0c1-ea76-431f-8cb0-0599eb51f928	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7488	6476	SEVERE CYCLONIC STORMS (N. INDIAN)	58ddb82c-fbb2-4910-8259-d9c2df2555da	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7489	6476	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	dd54dfac-069b-4552-abfe-d182320189c7	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7490	6476	TYPHOONS (WESTERN N. PACIFIC)	53998f98-9bf6-4666-90c7-48f2e5730dae	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM 1-MINUTE SUSTAINED WIND > TYPHOONS (WESTERN N. PACIFIC)	1
7491	6477	CYCLONES (SW INDIAN)	b5965fe4-fc00-4d9b-93f8-f03a6a369304	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND > CYCLONES (SW INDIAN)	1
7492	6477	HURRICANES  (N. ATLANTIC/E. PACIFIC)	8807cdb6-56af-43d6-9efa-14d234d69374	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7493	6477	SEVERE CYCLONIC STORMS (N. INDIAN)	40f7445f-1741-418e-9831-e2e3322daf5a	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7606	6637	HEADWATER STREAM	de9222a5-c3bc-470d-86dc-8b426ce61b76	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM > HEADWATER STREAM	1
7494	6477	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	a8258a99-866f-4e34-80ab-25239546ffb2	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7495	6477	TYPHOONS (WESTERN N. PACIFIC)	8e93861c-5f03-4892-96d7-cfac368e6c26	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM SURFACE WIND > TYPHOONS (WESTERN N. PACIFIC)	1
7496	6478	CYCLONES (SW INDIAN)	d5f307ab-e5df-4c84-84e7-42822e3a4864	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST > CYCLONES (SW INDIAN)	1
7497	6478	HURRICANES  (N. ATLANTIC/E. PACIFIC)	2d2a56cb-a99c-4001-9f41-0e04037e0d41	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7498	6478	SEVERE CYCLONIC STORMS (N. INDIAN)	6e28bebd-0c5d-4bf3-8770-84d79c75e33c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7499	6478	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	4379a82a-c0fd-4d40-b1f3-3b516cac1a8e	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7500	6478	TYPHOONS (WESTERN N. PACIFIC)	536b666d-a4ad-4ec3-b7fc-282e884e53ee	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MAXIMUM WIND GUST > TYPHOONS (WESTERN N. PACIFIC)	1
7501	6479	CYCLONES (SW INDIAN)	ef467c3c-0aed-4aa8-bfa5-67721e83e557	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > CYCLONES (SW INDIAN)	1
7502	6479	HURRICANES  (N. ATLANTIC/E. PACIFIC)	3b1544bc-1711-4553-a643-5d8fba38a1f1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7503	6479	SEVERE CYCLONIC STORMS (N. INDIAN)	50abff20-11a8-4aea-8425-c9a05b1d8d09	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7504	6479	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	5b70e02b-0ed2-42a0-9fe9-7a552d6819d1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7505	6479	TYPHOONS (WESTERN N. PACIFIC)	cfb85bf2-9920-4e3f-bce3-3d8f68ab1436	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > TYPHOONS (WESTERN N. PACIFIC)	1
7506	6480	CYCLONES (SW INDIAN)	d038c99b-efbc-41f3-99a6-5d066fda5ecd	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY > CYCLONES (SW INDIAN)	1
7507	6480	HURRICANES  (N. ATLANTIC/E. PACIFIC)	5730c1ba-7e4e-4d0e-adf3-053af4be97b4	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7508	6480	SEVERE CYCLONIC STORMS (N. INDIAN)	b21b9b00-5da4-47fc-b2a8-fc2ecd5bd912	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7509	6480	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	cbe89018-3eb6-4c8e-82c9-c540147a75e2	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7510	6480	TYPHOONS (WESTERN N. PACIFIC)	20da8cba-3546-4699-8809-01bffa6bccca	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > PEAK INTENSITY > TYPHOONS (WESTERN N. PACIFIC)	1
7511	6481	HURRICANES  (N. ATLANTIC/E. PACIFIC)	c6ff6623-a24c-494c-804c-bc486b3de548	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 1) > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7512	6482	HURRICANES  (N. ATLANTIC/E. PACIFIC)	fe4f3f33-7df3-439a-9382-d02140da29aa	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 2) > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7513	6483	HURRICANES  (N. ATLANTIC/E. PACIFIC)	d678b2d9-9956-45a9-9a9f-95450fb4ca46	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 3) > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7514	6484	HURRICANES  (N. ATLANTIC/E. PACIFIC)	91843b75-9519-456a-89a5-1b1c221ebd4e	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 4) > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7515	6485	HURRICANES  (N. ATLANTIC/E. PACIFIC)	6f80bcdf-b778-4ecc-99aa-9f5779fd6f31	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > SAFFIR-SIMPSON SCALE AT LANDFALL (CATEGORY 5) > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7516	6486	CYCLONES (SW INDIAN)	00d89979-f1bb-4e95-b73e-6a0d8d924bd8	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT > CYCLONES (SW INDIAN)	1
7517	6486	HURRICANES  (N. ATLANTIC/E. PACIFIC)	d99d0464-db69-44fb-9b18-9469a08fe4b4	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7518	6486	SEVERE CYCLONIC STORMS (N. INDIAN)	ed71cef0-0e5a-49a0-83c6-f7dd02215290	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7519	6486	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	713123e4-ebc8-49dd-bc8b-b9fbeaabeaad	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7520	6486	TYPHOONS (WESTERN N. PACIFIC)	6ee22b9c-f418-4b77-bb6b-f70d3e44afbc	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE FORCE WIND EXTENT > TYPHOONS (WESTERN N. PACIFIC)	1
7521	6488	CYCLONES (SW INDIAN)	63e53301-d263-4d09-a4be-f0c874646e23	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION > CYCLONES (SW INDIAN)	1
7522	6488	HURRICANES  (N. ATLANTIC/E. PACIFIC)	a8a40309-c4e5-46d7-ac39-1b7230766192	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7523	6488	SEVERE CYCLONIC STORMS (N. INDIAN)	446a22b7-3ea1-43db-9176-47d4dac3ac93	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7524	6488	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	7705e65c-90a1-451d-8898-ef5f170fa051	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7525	6488	TYPHOONS (WESTERN N. PACIFIC)	93ef0499-0b06-4f9a-885b-52e89563b3ec	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE MOTION > TYPHOONS (WESTERN N. PACIFIC)	1
7526	6489	CYCLONES (SW INDIAN)	f4f4a7ad-73da-42f2-94f9-d9ecb81e0bf0	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS > CYCLONES (SW INDIAN)	1
7527	6489	HURRICANES  (N. ATLANTIC/E. PACIFIC)	41829fbf-2b76-4714-bf4a-e0d63b5472d5	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7528	6489	SEVERE CYCLONIC STORMS (N. INDIAN)	9928589d-0714-4b88-a8ad-11126dd97521	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7529	6489	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	5d51ef9b-f058-48ca-b1ea-c8d63a50a699	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7530	6489	TYPHOONS (WESTERN N. PACIFIC)	09849cf3-df4d-40d3-a224-f30c6fe22c1f	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE RADIUS > TYPHOONS (WESTERN N. PACIFIC)	1
7531	6490	CYCLONES (SW INDIAN)	5d0a21f1-cc5d-481c-ad5f-7fe15deabc9c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK > CYCLONES (SW INDIAN)	1
7532	6490	HURRICANES  (N. ATLANTIC/E. PACIFIC)	72de9813-4c72-45bc-a216-be6ebd08bb6c	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK > HURRICANES  (N. ATLANTIC/E. PACIFIC)	1
7533	6490	SEVERE CYCLONIC STORMS (N. INDIAN)	e61fcc9f-bdb6-4dbc-94f2-52c4c64b6df9	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK > SEVERE CYCLONIC STORMS (N. INDIAN)	1
7534	6490	SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	8d27af08-6b2f-48d7-8e6b-bd57e93992ad	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK > SEVERE TROPICAL CYCLONES (SW PACIFIC/SE INDIAN)	1
7535	6490	TYPHOONS (WESTERN N. PACIFIC)	b5a681af-5005-4182-922e-528ec8d514f1	EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > TROPICAL CYCLONE TRACK > TYPHOONS (WESTERN N. PACIFIC)	1
7536	6502	ARACHNIDS	973bd2bd-c201-4e8c-8c86-d2e849298310	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CHELICERATES > ARACHNIDS	1
7537	6503	AMPHIPODS	e20c4981-7cbe-4f5c-9139-78b22ee7bfb6	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > AMPHIPODS	1
7538	6503	BARNACLES	57e04385-5f7b-432b-8f0b-b26fc9e3d77d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > BARNACLES	1
7539	6503	COPEPODS	9443e3fb-5087-4aae-a311-35ab172c45ce	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > COPEPODS	1
7540	6503	DECAPODS	e631c681-5dad-48b2-83ce-943a1f0df47a	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > DECAPODS	1
7541	6503	EUPHAUSIIDS (KRILL)	4095dea9-3da1-4679-bccf-7fe637414910	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > EUPHAUSIIDS (KRILL)	1
7542	6503	ISOPODS	dcf06e40-74f1-4341-bc80-79dcd2e268b9	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > ISOPODS	1
7543	6503	MYSIDS	bfda8569-896e-4efa-81e1-8f02af8b1017	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > MYSIDS	1
7544	6503	OSTRACODS	e91ca626-7afa-4e36-8a28-f8df6fc9d797	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > CRUSTACEANS > OSTRACODS	1
7545	6504	ENTOGNATHA	b23a3120-0b90-434d-81e6-988f62034e22	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > HEXAPODS > ENTOGNATHA	1
7546	6504	INSECTS	44e49605-e860-41d0-8ef8-cb74419f831d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > HEXAPODS > INSECTS	1
7547	6487	CENTIPEDES	582efbf1-ae9c-47f4-8155-c445f3816dd8	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > MYRIAPODS > CENTIPEDES	1
7548	6487	MILLIPEDES	d6db51cf-d2d0-4203-94c8-c884579e0cb0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > ARTHROPODS > MYRIAPODS > MILLIPEDES	1
7549	6505	HARD OR STONY CORALS	dd4de9c8-e078-43cf-a7d8-78f289c8618e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/HEXACORALS > HARD OR STONY CORALS	1
7550	6505	SEA ANEMONES	9c47c3f3-09ae-491f-994c-0322e2875a7e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/HEXACORALS > SEA ANEMONES	1
7551	6506	SEA FANS/SEA WHIPS	c6b33bb7-9714-42b5-88d2-f16bd671b799	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/OCTOCORALS > SEA FANS/SEA WHIPS	1
7552	6506	SEA PENS	9f25a6bc-ccbd-44fd-a33f-36a2ed53827f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/OCTOCORALS > SEA PENS	1
7553	6506	SOFT CORALS	7836e8bd-176d-4e2f-9ac1-7f9d9a152b4e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > CNIDARIANS > ANTHOZOANS/OCTOCORALS > SOFT CORALS	1
7554	6513	CLAMS	9273a48a-7ca4-4f1a-9347-7f6599b5a7e3	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > BIVALVES > CLAMS	1
7555	6513	MUSSELS	bc60fbb8-f9e9-492e-9acf-0f47345cedf2	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > BIVALVES > MUSSELS	1
7556	6513	OYSTERS	b6782a30-639e-4d70-8290-81683d248b1f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > BIVALVES > OYSTERS	1
7557	6514	SQUIDS	0d07a910-06bf-4607-90f8-422e1f35cfa0	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/INVERTEBRATES > MOLLUSKS > CEPHALOPODS > SQUIDS	1
7558	6539	ANCHOVIES/HERRINGS	4309af7d-76c8-4856-8ed3-20693600228b	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > ANCHOVIES/HERRINGS	1
7559	6539	CATFISHES/MINNOWS	89530978-556a-44fd-88fa-5d42ce9c8b91	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > CATFISHES/MINNOWS	1
7560	6539	CODS/HADDOCKS	340b843e-841e-40d9-97c2-d76cca66c65e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > CODS/HADDOCKS	1
7561	6539	FLOUNDERS	74b0e517-8cde-45ad-b6fa-0849d4355928	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > FLOUNDERS	1
7562	6539	NEEDLEFISHES	4b9b8b32-93b4-4e8e-819d-55ee7f6a6480	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > NEEDLEFISHES	1
7563	6539	PERCH-LIKE FISHES	85b2ba83-b81c-45a6-98d1-07b36040fe45	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > PERCH-LIKE FISHES	1
7564	6539	PUPFISHES	3179b46a-ce20-453c-9ebf-18a070a91dec	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > PUPFISHES	1
7565	6539	SALMONS/TROUTS	0b8d5346-d10b-4e32-8179-7a51970c5e7f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > SALMONS/TROUTS	1
7566	6539	STURGEONS/PADDLEFISHES	01549b6d-91e1-40de-bd7c-5ed5ee59d14e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > STURGEONS/PADDLEFISHES	1
7567	6542	BEARS	6831004a-34d7-42f5-a903-6c84a5e7590f	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES > BEARS	1
7568	6542	DOGS/FOXES/WOLVES	8d01f599-3a98-44b9-889f-43df92386d12	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES > DOGS/FOXES/WOLVES	1
7569	6542	MARTENS/WEASELS/WOLVERINES	d8973cd1-f3b4-4087-bf3b-25ac0732fb38	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES > MARTENS/WEASELS/WOLVERINES	1
7570	6542	OTTERS	eedb68d2-c487-4dc8-8292-c375e3e8b455	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES > OTTERS	1
7571	6542	SEALS/SEA LIONS/WALRUSES	35cf1beb-a654-4ceb-ab6b-7e505c2144e7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CARNIVORES > SEALS/SEA LIONS/WALRUSES	1
7572	6543	BALEEN WHALES	5e0ce993-df7c-46e2-9942-3a242df75705	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CETACEANS > BALEEN WHALES	1
7573	6543	TOOTHED WHALES	1e2a4882-d1e9-4e1a-a2a5-efc449133bf5	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > CETACEANS > TOOTHED WHALES	1
7574	6546	CATTLE/SHEEP	33e2e026-e40b-4932-95a9-b2ca1a7aa407	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > EVEN-TOED UNGULATES > CATTLE/SHEEP	1
7575	6546	DEER/MOOSE	5557a4f3-8392-4df5-81a9-206c2a86da89	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > EVEN-TOED UNGULATES > DEER/MOOSE	1
7576	6546	HOGS/PIGS	108ece15-4588-4564-b803-dc1c17cf193e	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > MAMMALS > EVEN-TOED UNGULATES > HOGS/PIGS	1
7577	6552	SEAGRASS	e36c5faa-c772-4bb0-aeca-b361e160ce9d	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > ANGIOSPERMS (FLOWERING PLANTS) > MONOCOTS > SEAGRASS	1
7578	6567	COCCOLITHOPHORES	ab7eb13f-5fcb-4afa-8819-c37d36feeec1	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PLANTS > MICROALGAE > HAPTOPHYTES > COCCOLITHOPHORES	1
7579	6573	COCCOLITHOPHORES	e88cc54b-7a4b-4680-b441-4d10a4534cd9	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > PROTISTS > FLAGELLATES > HAPTOPHYTES > COCCOLITHOPHORES	1
7580	6631	CROPLAND	2c74f390-9d82-4903-98e0-bddf0d3247fb	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > AGRICULTURAL LANDS > CROPLAND	1
7581	6631	FOREST PLANTATION	39fee18c-8572-4d72-a0ce-2a72942c4870	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > AGRICULTURAL LANDS > FOREST PLANTATION	1
7582	6631	PASTURE	46a26fc7-95f0-409e-8bfa-eb623b3a3f8d	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > AGRICULTURAL LANDS > PASTURE	1
7583	6631	RANGELAND	3c8b236c-de02-491b-a506-91ecdc324a1c	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > AGRICULTURAL LANDS > RANGELAND	1
7584	6632	MINNING/DRILLING SITE	7d8dcf2c-133f-47b2-9195-17dd263ec8a3	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > RESOURCE DEVELOPMENT SITE > MINNING/DRILLING SITE	1
7585	6632	SOLAR FARM	9ff1f885-108f-40cb-a054-4e076b8d648b	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > RESOURCE DEVELOPMENT SITE > SOLAR FARM	1
7586	6632	WATER IMPOUNDMENT	39fa5f62-1c4e-4790-a768-1252c0b51c7b	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > RESOURCE DEVELOPMENT SITE > WATER IMPOUNDMENT	1
7587	6632	WIND FARM	0c603a5b-d5e9-4e87-a8dc-2af456678dba	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > RESOURCE DEVELOPMENT SITE > WIND FARM	1
7588	6633	CANAL	a0c33d15-b76c-4a0d-abb7-6919102b2977	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > URBAN LANDS > CANAL	1
7589	6633	GARDEN	3bd03ca9-4a63-44f1-b368-36f2400776e6	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > URBAN LANDS > GARDEN	1
7590	6633	PARK	2b1f7993-2d54-40de-abc4-3909f619ad4e	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > URBAN LANDS > PARK	1
7591	6633	ROADSIDE	a9f2e036-f04f-46cc-a4e8-dfba30d9034c	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > ANTHROPOGENIC/HUMAN INFLUENCED ECOSYSTEMS > URBAN LANDS > ROADSIDE	1
7592	6634	PHYTOPLANKTON	235996b1-b1a8-4c20-bb1f-711fb1a0c952	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > PLANKTON > PHYTOPLANKTON	1
7593	6634	ZOOPLANKTON	0399b52c-e3de-4dcc-9eb6-b1e3acf2cf1b	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > PLANKTON > ZOOPLANKTON	1
7594	6635	ESTUARINE WETLANDS	3e924e3a-eb5d-4f81-8981-1b9f622ddc82	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > ESTUARINE WETLANDS	1
7595	6635	LACUSTRINE WETLANDS	dd22cc67-afd5-4b9e-8072-90651a191486	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > LACUSTRINE WETLANDS	1
7596	6635	MARINE	bc320625-d9ba-41f5-9336-57e86fd878f3	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > MARINE	1
7597	6635	MARSHES	291a51b8-07e5-4a66-8140-d140d69843db	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > MARSHES	1
7598	6635	PALUSTRINE WETLANDS	d400ab07-bde9-40cc-b70a-63eda730eab2	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > PALUSTRINE WETLANDS	1
7599	6635	PEATLANDS	b70ef20c-7215-4a39-9479-dbff7c2fdca9	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > PEATLANDS	1
7600	6635	RIPARIAN WETLANDS	41446bdc-89f6-4d84-a2a4-005390757235	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > RIPARIAN WETLANDS	1
7601	6635	SWAMPS	6cec3b57-1a7f-404d-afde-4de045ef0dd2	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > SWAMPS	1
7602	6635	VERNAL POOL	e72c39c5-5480-4602-bb37-216b5cc737dd	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > AQUATIC ECOSYSTEMS > WETLANDS > VERNAL POOL	1
7603	6636	MONTANE LAKE	b23b9a47-d2aa-4e67-84d6-5fe2527d6fb6	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > LAKE/POND > MONTANE LAKE	1
7604	6636	SALINE LAKES	06a2da0f-5234-4d29-905b-153d88657eb9	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > LAKE/POND > SALINE LAKES	1
7605	6637	EPHEMERAL STREAM	5f76c978-1c8a-496e-bc6a-78ff7656f014	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM > EPHEMERAL STREAM	1
7607	6637	INTERMITTENT STREAM	1b5d3b68-4f89-4772-b015-ce6f30cf0496	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM > INTERMITTENT STREAM	1
7608	6637	PERENNIAL STREAM/RIVER	0236a2e0-64d6-4763-bcd1-ea8bb3a117a1	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM > PERENNIAL STREAM/RIVER	1
7609	6637	RIVER DELTA	bafaa203-0dc0-4167-a64a-d89ba16d8eb1	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > FRESHWATER ECOSYSTEMS > RIVERS/STREAM > RIVER DELTA	1
7611	6638	HYDROTHERMAL VENT	bee69b66-3921-4883-920f-6a0bd85b614f	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ABYSSAL > HYDROTHERMAL VENT	1
7612	6640	BEACHES	a61d1705-a6b7-4df3-9f8e-57e26029629c	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > BEACHES	1
7613	6640	DUNES	8d38de3b-2d05-4ad2-a960-f47a66191319	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > DUNES	1
7614	6640	KELP FOREST	d609fc5c-8267-4e79-84ec-93629d52aba8	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > KELP FOREST	1
7615	6640	LAGOON	879d286b-9ea6-4e4d-bdd1-56a4c7ca1531	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > LAGOON	1
7616	6640	MANGROVE SWAMP	7c666111-3297-474b-ba7b-c93db3a52cb0	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > MANGROVE SWAMP	1
7617	6640	MUDFLAT	771b2919-ab55-4c71-8561-b4fb365da53f	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > MUDFLAT	1
7618	6640	ROCKY INTERTIDAL	80e51854-2f3f-447e-9786-6d2ccb0dd886	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > ROCKY INTERTIDAL	1
7619	6640	SALT MARSH	fbe91a4f-4d27-4cfe-ba1b-69a62e359a3d	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > SALT MARSH	1
7620	6640	SAV/SEA GRASS BED	9d0e3045-943e-460c-8bef-1db6fbf76341	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > COASTAL > SAV/SEA GRASS BED	1
7621	6642	BRACKISH MARSH	155e730b-4e22-4962-adc5-a4b92543a442	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ESTUARY > BRACKISH MARSH	1
7622	6642	MANGROVE SWAMP	63cd8427-07bd-4a46-b725-ca65da4bf9b6	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ESTUARY > MANGROVE SWAMP	1
7623	6642	MUDFLAT	86987ad2-21d2-496b-9119-350b3fb17455	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ESTUARY > MUDFLAT	1
7624	6642	SAV/SEA GRASS BED	5f6e1b08-caca-423b-80dc-7de3da7a2988	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > ESTUARY > SAV/SEA GRASS BED	1
7625	6643	NERITIC ZONE	eb958dfb-5e38-401f-8b42-5f1273c75a4a	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > PELAGIC > NERITIC ZONE	1
7626	6643	OCEANIC ZONE	02d78090-d0b5-490d-92a8-b593172ab232	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > PELAGIC > OCEANIC ZONE	1
7627	6644	CORAL REEF	fa3bc02d-31a7-4456-b716-a8b8f8393c86	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > REEF > CORAL REEF	1
7628	6644	OYSTER REEF	758c00c3-03a3-4cef-9248-ab392d789148	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > MARINE ECOSYSTEMS > REEF > OYSTER REEF	1
7629	6645	ALPINE TUNDRA	944d9d09-4317-4e9a-9aa5-dc4282be406e	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > ALPINE/TUNDRA > ALPINE TUNDRA	1
7630	6645	ARCTIC TUNDRA	46ecf46f-a710-4589-82b2-34aebf35c3c0	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > ALPINE/TUNDRA > ARCTIC TUNDRA	1
7631	6645	SUBALPINE	101950b9-00d3-4721-9af8-fa5d51b196c3	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > ALPINE/TUNDRA > SUBALPINE	1
7632	6647	DESERT SCRUB	4f63746e-0e8b-4254-9d4a-a23a852f819f	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > DESERTS > DESERT SCRUB	1
7633	6648	BOREAL FOREST/TIAGA	cafa8131-4a2d-4c8b-811c-0d64adf5fc06	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > BOREAL FOREST/TIAGA	1
7634	6648	TEMPERATE CONIFEROUS FOREST	5d8236b5-bf5b-499f-a8e7-0cd80e00d261	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > TEMPERATE CONIFEROUS FOREST	1
7635	6648	TEMPERATE DECIDUOUS FOREST	a59dc6dc-5348-4e8b-aec2-20cdeb38b617	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > TEMPERATE DECIDUOUS FOREST	1
7636	6648	TEMPERATE MIXED FOREST	9cde47e7-325b-465e-93a6-ae4d459c7945	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > TEMPERATE MIXED FOREST	1
7637	6648	TEMPERATE RAINFOREST	96ea0bde-7cf6-4601-8a49-116636f556cf	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > TEMPERATE RAINFOREST	1
7638	6648	TROPICAL RAINFOREST	89bb4e2b-dd39-44ed-a4d3-2b205e9fa68a	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > FORESTS > TROPICAL RAINFOREST	1
7639	6649	MONTANE GRASSLAND	ddb4ca0c-9b19-442d-8bcc-e664544d3fe9	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > GRASSLANDS > MONTANE GRASSLAND	1
7640	6649	SAVANNA	d58dab07-f57e-47a9-8dcf-02a3e17f3533	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > GRASSLANDS > SAVANNA	1
7641	6654	CHAPARRAL	0cc6527e-d162-4951-9db7-a6afe5c631c0	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > SHRUBLAND/SCRUB > CHAPARRAL	1
7642	6654	MONTANE SHRUBLAND	9409e1f9-f3a9-46fa-aaf9-0e685ca2adcb	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > SHRUBLAND/SCRUB > MONTANE SHRUBLAND	1
7643	6655	ESTUARINE WETLANDS	0e1f3f95-58b5-4f10-b239-850c66ed55ff	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > ESTUARINE WETLANDS	1
7644	6655	LACUSTRINE WETLANDS	686e66f7-27bf-4b67-b034-e0fdf0e47c0c	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > LACUSTRINE WETLANDS	1
7645	6655	MARINE	8ef6f360-10d0-4dc5-8fcb-c532eb23fe5d	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > MARINE	1
7646	6655	MARSHES	419877cb-0c17-44b0-9b3d-a2283887a7a6	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > MARSHES	1
7647	6655	PALUSTRINE WETLANDS	6862d4d4-51fe-4fde-80eb-60d3ef08e88e	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > PALUSTRINE WETLANDS	1
7648	6655	PEATLANDS	f3b5489d-6723-40bf-bd55-68a0f2fc1874	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > PEATLANDS	1
7649	6655	RIPARIAN WETLANDS	1af675ae-9a65-4d91-970e-a8b9fcce0232	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > RIPARIAN WETLANDS	1
7650	6655	SWAMPS	8c05bcf2-d13b-44fd-b1a2-5ec797b2f851	EARTH SCIENCE > BIOSPHERE > ECOSYSTEMS > TERRESTRIAL ECOSYSTEMS > WETLANDS > SWAMPS	1
7651	6668	THI	9130e78a-882c-4a69-b1ae-0b775869c3de	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES > TEMPERATURE-HUMIDITY INDEX > THI	1
7652	6669	WTVI	bcd11fd2-ddf4-4cd3-8507-c3bf6f40a934	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > HUMIDITY INDICES > WATER VAPOR TRANSPORT INDEX > WTVI	1
7653	6670	CUI	db8eb32d-2f86-40ab-82af-b615b5a30db9	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > OCEAN UPWELLING INDICES > OCEAN COASTAL UPWELLING INDEX > CUI	1
7654	6681	CAR	b7ad62e0-f904-4429-b6db-6cc50b2281bc	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > CARIBBEAN INDEX > CAR	1
7655	6682	NINO 4 INDEX	f59ce66b-a76d-467c-bab1-6264f9f3bb70	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > CENTRAL TROPICAL PACIFIC SST > NINO 4 INDEX	1
7656	6683	NINO 3.4 INDEX	a084d58c-c4f6-40fa-a645-96d9bef021aa	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > EAST CENTRAL TROPICAL PACIFIC SST > NINO 3.4 INDEX	1
7657	6684	NINO 1+2 INDEX	1c2e9a42-39d1-4b38-b752-3982f2a36ef4	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > EXTREME EASTERN TROPICAL PACIFIC SST > NINO 1+2 INDEX	1
7658	6687	NTA	85586d78-1819-4ba7-ab5f-9f684640d730	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > NORTH TROPICAL ATLANTIC INDEX > NTA	1
7659	6688	ONI	fbae11f2-f8db-44b8-bcb6-55471dca13a2	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > OCEANIC NINO INDEX > ONI	1
7660	6690	TNI	aaa9c9eb-9d46-4015-a735-8938e0ed4506	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TRANS-NINO INDEX > TNI	1
7661	6691	TNA	88841897-1e84-4df0-a677-2da7adc3ce37	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TROPICAL NORTH ATLANTIC INDEX > TNA	1
7662	6693	TSA	b625d811-6c7e-4204-abc8-2c72d07aba02	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > TROPICAL SOUTH ATLANTIC INDEX > TSA	1
7663	6694	WHWP	1bbb19ba-49b7-47c2-b8c8-fa61bb615fb3	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > SEA SURFACE TEMPERATURE INDICES > WESTERN HEMISPHERE WARM POOL > WHWP	1
7664	6695	AAO	690be4e9-c48c-4442-8b86-3d0a51abb0c1	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ANTARCTIC OSCILLATION > AAO	1
7665	6696	AO	a135fceb-cf13-4186-9ad3-8d5db82312c9	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ARCTIC OSCILLATION > AO	1
7666	6697	AMM	ddcc55bd-2047-4aa2-996c-409f940fbba9	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ATLANTIC MERIDIONAL MODE > AMM	1
7667	6698	AMO	cc579f1f-6a72-425b-84c3-aa8070d4a0ec	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > ATLANTIC MULTIDECADAL OSCILLATION LONG VERSION > AMO	1
7668	6699	BEST	94ecf3ab-aa20-4756-8e3b-629795b3d5b5	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > BIVARIATE ENSO TIMESERIES INDEX > BEST	1
7669	6701	EA-JET	45dd0a01-d428-4407-ba18-c074d3172b41	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EAST ATLANTIC JET PATTERN > EA-JET	1
7670	6702	EATL	739f9b7e-3ca7-4f0b-8ce2-68753fc0a6d9	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EAST ATLANTIC PATTERN > EATL	1
7671	6703	EATL/WRUS	bae01a02-ff03-4ad8-9080-3a4f89fa0dc6	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EASTERN ATLANTIC WESTERN RUSSIA PATTERN > EATL/WRUS	1
7672	6704	EP/NP	334d9428-a178-4a5e-b758-a3675a122bef	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EASTERN PACIFIC OSCILLATION > EP/NP	1
7673	6705	ENSO	54330626-f9b4-4c34-949a-9be427fdf51b	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > EL NINO SOUTHERN OSCILLATION (ENSO) > ENSO	1
7674	6709	MJO	2953da71-fe1d-4506-9bd6-445b92e2b443	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > MADDEN-JULIAN OSCILLATION > MJO	1
7675	6710	MEI	087bffd1-f4f5-49ef-98d8-8e7d1169bfe8	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > MULTIVARIATE ENSO INDEX > MEI	1
7676	6711	NAO	19631138-70c8-4922-8052-821ec5ce093b	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH ATLANTIC OSCILLATION > NAO	1
7677	6712	NPO	b362dfd4-3901-4db9-9e39-bb29b6dad621	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH PACIFIC OSCILLATION > NPO	1
7678	6713	NP	34b92cc2-7708-4e44-8c3f-4c23f62be944	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTH PACIFIC PATTERN > NP	1
7679	6714	NOI	9a43235b-a7b7-4c76-b296-c01799b1f278	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > NORTHERN OSCILLATION INDEX > NOI	1
7680	6715	PDO	8a31313b-e60e-47e8-b7bd-df0503e7c868	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > PACIFIC DECADAL OSCILLATION > PDO	1
7681	6716	PNA	ebddda06-097f-4454-9751-bb27c41aca37	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > PACIFIC/NORTH AMERICAN (PNA) PATTERN > PNA	1
7682	6717	PT	15f42cd5-9822-4769-be88-3efe64205ce0	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > Pacific Transition Index > PT	1
7683	6718	QBO	e932c1de-a7b5-4cbc-9f56-a40234334b2e	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > QUASI-BIENNIAL OSCILLATION > QBO	1
7684	6719	SOI	cafeff8b-c583-40e3-9a43-2b2b069b1df8	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > SOUTHERN OSCILLATION INDEX > SOI	1
7685	6720	TNH	8eac6c91-8af5-4b1b-8dc3-89cd4871915f	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > TROPICAL/NORTHERN HEMISPHERE PATTERN > TNH	1
7686	6721	WP	fe25c265-296d-4671-9e66-9b752b78bb60	EARTH SCIENCE > CLIMATE INDICATORS > ATMOSPHERIC/OCEAN INDICATORS > TELECONNECTIONS > WEST PACIFIC INDEX > WP	1
7687	6760	ISOTOPIC ANALYSIS	bd1834b0-4f8f-4616-b330-6205bff567c2	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > TREE RINGS > ISOTOPIC ANALYSIS	1
7688	6765	ARGON ISOTOPES	6a0fc2ec-d1cf-43b5-8e97-6ab96811c02b	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ISOTOPES > ARGON ISOTOPES	1
7689	6765	NITROGEN ISOTOPES	e1138bec-7087-45f4-82b0-2e4029063381	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ISOTOPES > NITROGEN ISOTOPES	1
7690	6765	OXYGEN ISOTOPES	a1362cee-634d-40f4-b47f-901b328895c3	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > ISOTOPES > OXYGEN ISOTOPES	1
7691	6768	MICROPARTICLE CONCENTRATION	84b443b5-91d3-42d2-a48b-d2e157a39d5b	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > ICE CORE RECORDS > PARTICULATE MATTER > MICROPARTICLE CONCENTRATION	1
7692	6772	CHARCOAL SEDIMENT	a090a598-3ae6-4fc4-b248-97ec5226702a	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > FIRE HISTORY > CHARCOAL SEDIMENT	1
7693	6772	FIRE SCAR DATE	c9ba3275-2fe3-4619-b7c0-881d4f6fa34e	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > FIRE HISTORY > FIRE SCAR DATE	1
7694	6780	SEDIMENT THICKNESS	0d8fc6d8-eba5-4da1-9a78-d69c23d9d78d	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > LAND RECORDS > SEDIMENTS > SEDIMENT THICKNESS	1
7695	6793	SEDIMENT THICKNESS	6fb40553-a2ef-465a-b7d2-3401e3bfceac	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > OCEAN/LAKE RECORDS > SEDIMENTS > SEDIMENT THICKNESS	1
7696	6808	SEDIMENT THICKNESS	88735956-6d46-41e1-8cbb-5dba20c33d8c	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > PALEOCLIMATE RECONSTRUCTIONS > SEDIMENTS > SEDIMENT THICKNESS	1
7697	6816	RIFTS	8a8fa93e-6424-46dd-ae97-d8afbac41b89	EARTH SCIENCE > CRYOSPHERE > GLACIERS/ICE SHEETS > ICE SHEETS > ICE SHEET MEASUREMENTS > RIFTS	1
7698	6857	TELE-EPIDEMIOLOGY	d6cad59b-327e-4f3f-a664-706224c470f9	EARTH SCIENCE > HUMAN DIMENSIONS > PUBLIC HEALTH > DISEASES/EPIDEMICS > EPIDEMIOLOGY > TELE-EPIDEMIOLOGY	1
7699	6866	CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	f51acce1-eaf6-4de7-b279-5b58c3034aeb	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	1
7700	6866	DOME DUNE	cb6b9191-21ab-4a56-b43f-27e86f90f6d9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > DOME DUNE	1
7701	6866	LONGITUDINAL/LINEAR DUNE	b5ee3496-6910-4971-8539-5aa084bfa9e1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > LONGITUDINAL/LINEAR DUNE	1
7702	6866	PARABOLIC DUNE	c63be844-efa7-49f6-8089-c60111bbdffb	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > PARABOLIC DUNE	1
7703	6866	STAR DUNE	dc9dea65-e574-4bbb-9945-cd6d1cdbf6c1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > STAR DUNE	1
7704	6868	VENTIFACTS	dec3d35a-3ffa-4bea-b239-f8e74b498fb2	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION > VENTIFACTS	1
7705	6868	YARDANGS	dabc0fc5-acac-48df-b32e-02c9166e8385	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION > YARDANGS	1
7706	6872	LOESS	5ce16b97-c91c-420c-9701-33d19d50b286	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT > LOESS	1
7707	6872	MONADNOCK	abe3a81a-3bac-450b-8006-304bee055289	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT > MONADNOCK	1
7708	6873	SEDIMENT CHEMISTRY	9ea3e92d-f772-4f39-a615-08b0e062ee9d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7709	6873	SEDIMENT COMPOSITION	02916754-4814-48ea-b8fc-ef50d7a7c5b5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7710	6873	STRATIGRAPHIC SEQUENCE	a7b04d56-2a44-4a94-8d94-1911a7110f9d	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7711	6877	APRON REEF	6c78ed6a-2dbc-4ced-acc2-d0246e0afedd	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > APRON REEF	1
7712	6877	ATOLL REEF	8bbf1177-c74b-4f11-8f7d-40c5785312a1	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > ATOLL REEF	1
7713	6877	BANK REEF	9ea0dbd4-2af5-4520-a831-32ee04d02ecc	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > BANK REEF	1
7714	6877	BARRIER REEF	e125e285-b547-47ea-b566-5dffce2bbcbd	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > BARRIER REEF	1
7715	6877	FRINGING REEF	b54234a2-3261-4c6e-8fd8-75230f3488c0	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > FRINGING REEF	1
7716	6877	PATCH REEF	a722fea3-fe54-4995-8aec-407efe20dee9	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > PATCH REEF	1
7717	6877	RIBBON REEF	7f674559-6e36-4a13-ac0c-f61aa6a37d63	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > RIBBON REEF	1
7718	6877	TABLE REEF	ec0692d8-1cce-4c89-a6ef-c35a5f812121	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > TABLE REEF	1
7719	6880	CRESCENTIC (BARCHAN/TRANSVERSE)	f8b39934-bdce-4f90-8b86-a001c0af8b76	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > CRESCENTIC (BARCHAN/TRANSVERSE)	1
7720	6880	DOME DUNE	8971f15d-bee3-4eaf-a7dd-ceb005448b37	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > DOME DUNE	1
7721	6880	LONGITUDINAL/LINEAR DUNE	386f4f36-26bd-4193-aa25-0c0ec2e5baae	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > LONGITUDINAL/LINEAR DUNE	1
7722	6880	PARABOLIC DUNE	db89fdd2-d911-4a75-9210-ce90db043358	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > PARABOLIC DUNE	1
7723	6880	STAR DUNE	5a271522-fee4-4646-9c9a-a99385f00d9f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > STAR DUNE	1
7724	6908	SEDIMENT CHEMISTRY	786c08f1-f3ed-4edd-8ec9-a69313906426	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7725	6908	SEDIMENT COMPOSITION	40d7f7e1-e11a-410b-a1b6-78c4a961d631	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7726	6908	STRATIGRAPHIC SEQUENCE	870803f5-8bbc-4e39-8372-ce21b0decb75	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7727	6941	V SHAPED VALLEY	186a08ed-b6fc-4963-adb6-2c5113d133e5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > VALLEY > V SHAPED VALLEY	1
7728	6953	SEDIMENT CHEMISTRY	ba0630cb-9a7e-4c4b-9675-c92aba7088ce	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7729	6953	SEDIMENT COMPOSITION	b976820e-6b8c-45f7-87a6-fa6474d39a35	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7730	6953	STRATIGRAPHIC SEQUENCE	e9c6d45a-787e-4099-bbf9-03d377cdb8d5	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7731	6958	LONGITUDINAL CREVASSES	a78c3d42-ac89-4040-9f0d-4d864b8c4551	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > LONGITUDINAL CREVASSES	1
7732	6958	MARGINAL CREVASSES	f0bbea2f-2ef0-4e99-ad76-1aedbbedc016	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > MARGINAL CREVASSES	1
7733	6958	TRANSVERSE CREVASSES	6ba069ae-8561-44b7-9e59-d645d6bd725f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > TRANSVERSE CREVASSES	1
7734	6970	LATERAL MORAINE	d3ad1ced-39fa-4e3a-a75d-58e5393a2abe	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > LATERAL MORAINE	1
7735	6970	MEDIAL MORAINE	063fae56-f066-4023-84c2-daff8261b7fc	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > MEDIAL MORAINE	1
7736	6970	RECESSIONAL MORAINE	5c242e01-40c4-4fca-a99d-48e4064f6c6f	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > RECESSIONAL MORAINE	1
7737	6970	RIBBED/ROGAN MORAINE	b62123dd-1bf5-4222-a646-05d71d729c75	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > RIBBED/ROGAN MORAINE	1
7738	6970	TERMINAL MORAINE	16bd425e-9a14-41ac-900e-5b5c4f713dda	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > TERMINAL MORAINE	1
7739	6983	BASAL ICE FREEZING	ee8dfdf6-0153-4067-ab3b-51794b01ee86	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FREEZE/THAW > BASAL ICE FREEZING	1
7740	6993	SEDIMENT CHEMISTRY	134fd984-9b26-4ceb-9084-3bffc0c5a321	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7741	6993	STRATIGRAPHIC SEQUENCE	7fa9d5ef-690e-4daf-8503-363b6b1cb6e4	EARTH SCIENCE > LAND SURFACE > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7742	7027	NORMALIZED DIFFERENCE VEGETATION INDEX (NDVI)	7b43eda3-899a-4afa-89be-2dbe527834c2	EARTH SCIENCE > LAND SURFACE > LAND USE/LAND COVER > LAND USE/LAND COVER CLASSIFICATION > VEGETATION INDEX > NORMALIZED DIFFERENCE VEGETATION INDEX (NDVI)	1
7743	7077	CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	5c80c047-c02e-4c15-83ac-26b8b1a8f114	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	1
7744	7077	DOME DUNE	d5ff7545-0eec-4cad-90a5-019e03cdac47	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > DOME DUNE	1
7745	7077	LONGITUDINAL/LINEAR DUNE	db2d6cfb-70c3-4568-99a0-a25b3c3879dd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > LONGITUDINAL/LINEAR DUNE	1
7746	7077	PARABOLIC DUNE	4cce9a44-da57-4169-b89f-6b1460fcedb9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > PARABOLIC DUNE	1
7747	7077	STAR DUNE	ce087840-ec71-4575-bca9-e807151cc376	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN LANDFORMS > DUNES > STAR DUNE	1
7748	7079	VENTIFACTS	2c15738b-839f-4b68-85bc-ece41e4ac6c9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION > VENTIFACTS	1
7749	7079	YARDANGS	59d1b0f7-ef02-4fa4-8d47-7eda39794713	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > ABRASION > YARDANGS	1
7750	7083	LOESS	a83052ef-9b98-4cb3-9bed-b0c9059812e5	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT > LOESS	1
7751	7083	MONADNOCK	8167592d-13bf-4225-9822-29e68bcd1b37	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENT TRANSPORT > MONADNOCK	1
7752	7084	SEDIMENT CHEMISTRY	34ea8c99-ff34-495b-b986-92a78b74a8e9	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7753	7084	SEDIMENT COMPOSITION	6e5a6d68-5f99-4f0d-bde3-9f24268af426	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7754	7084	STRATIGRAPHIC SEQUENCE	a08cce11-9407-4b1f-b13e-0df87da03612	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > AEOLIAN PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7755	7088	APRON REEF	0e566bce-90bf-4a0a-a000-5bb5fb430788	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > APRON REEF	1
7756	7088	ATOLL REEF	8c89ede4-94d8-4fd4-a3df-f9d42e9835eb	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > ATOLL REEF	1
7757	7088	BANK REEF	57417a5e-4d86-4fb6-81d6-68bf9a3d1148	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > BANK REEF	1
7758	7088	BARRIER REEF	5fde7781-d4f6-41a8-8428-f428b70c02dc	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > BARRIER REEF	1
7759	7088	FRINGING REEF	0f5c48d1-5189-495d-b5a7-7ad596f0a5c4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > FRINGING REEF	1
7760	7088	PATCH REEF	a1451fce-9e69-4f2d-b2cf-27238a7577ce	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > PATCH REEF	1
7761	7088	RIBBON REEF	b428ba89-4638-4989-90c1-f5e4f0d0a6f6	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > RIBBON REEF	1
7762	7088	TABLE REEF	5f4dc81d-0893-4eb9-b82a-6a070836aa16	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > CORAL REEFS > TABLE REEF	1
7763	7091	CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	fa47cab9-0aa4-4e16-8115-972f7f543920	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > CRESCENTIC (BARCHAN/TRANSVERSE) DUNE	1
7764	7091	DOME DUNE	16a1f6b8-ea67-43fe-a47c-aad5250b4f59	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > DOME DUNE	1
7765	7091	LONGITUDINAL/LINEAR DUNE	1810b08a-9377-4f01-a3cf-fdd549ad8ebf	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > LONGITUDINAL/LINEAR DUNE	1
7766	7091	PARABOLIC DUNE	174fa36e-3a06-40a1-bc95-87e6799bdead	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > PARABOLIC DUNE	1
7767	7091	STAR DUNE	94ab11dc-b70b-4705-bb25-c4d430722d28	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL LANDFORMS > DUNES > STAR DUNE	1
7768	7119	SEDIMENT CHEMISTRY	9f4548ad-ec40-4d79-a973-552b2541a62d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7769	7119	SEDIMENT COMPOSITION	17d6838d-e05e-4f0f-a751-7dbd00d2a80a	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7770	7119	STRAITRAPHIC SEQUENCE	1203f04d-cd90-4f46-b2c1-998a3c182250	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > SEDIMENTATION > STRAITRAPHIC SEQUENCE	1
7771	7125	DEGRADATION	2f5ceedb-afb6-47e6-8eac-8f220ef0b564	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > COASTAL PROCESSES > WAVE EROSION > DEGRADATION	1
7772	7152	V SHAPPED VALLEY	fdb4c687-916e-48ec-858e-6009cc763de3	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL LANDFORMS > VALLEY > V SHAPPED VALLEY	1
7773	7164	SEDIMENT CHEMISTRY	09b4427b-9e8b-413a-83cd-f087b284cf61	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7774	7164	SEDIMENT COMPOSITION	17747820-39de-4908-bb3d-8c2f94ddd6f4	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > SEDIMENT COMPOSITION	1
7775	7164	STRAITIGRAPHIC SEQUENCE	103f1165-1008-4caa-bf77-5259ae1a7a36	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > FLUVIAL PROCESSES > SEDIMENTATION > STRAITIGRAPHIC SEQUENCE	1
7776	7169	LONGITUDINAL CREVASSES	429d0eba-2689-4674-9a8a-d88c4058b1bf	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > LONGITUDINAL CREVASSES	1
7777	7169	MARGINAL CREVASSES	bc803dca-2fdb-4dc0-bf02-f0b9399d6816	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > MARGINAL CREVASSES	1
7778	7169	TRANSVERSE CREVASSES	45101ace-ce83-4b56-bea6-c4eca9c693dd	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > CREVASSES > TRANSVERSE CREVASSES	1
7779	7181	LATERAL MORAINE	a4f0e7c2-711e-4675-b7c8-f5430905aa89	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > LATERAL MORAINE	1
7780	7181	MEDIAL MORAINE	9d6c8fac-a5cd-4fbc-8283-1bc256c12a43	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > MEDIAL MORAINE	1
7781	7181	RECESSIONAL MORAINE	c4f0d15c-1f9b-40f3-b5d4-da1d6ebe6da8	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > RECESSIONAL MORAINE	1
7782	7181	RIBBED/ROGAN MORAINE	a389919c-a6da-465e-b074-ea29b66a686b	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > RIBBED/ROGAN MORAINE	1
7783	7181	TERMINAL MORAINE	7886c3eb-e86e-4a84-9f2f-e398ecc82b2d	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL LANDFORMS > MORAINES > TERMINAL MORAINE	1
7784	7194	BASAL ICE FREEZING	a72c8430-0b33-4167-b189-1309cc2048c5	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > FREEZE/THAW > BASAL ICE FREEZING	1
7785	7204	SEDIMENT CHEMISTRY	7d10ff6d-efde-4f97-866b-7d771dd32b25	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION > SEDIMENT CHEMISTRY	1
7786	7204	STRATIGRAPHIC SEQUENCE	c25fef4a-f346-4831-8015-7853886c4fc7	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > GLACIAL PROCESSES > SEDIMENTATION > STRATIGRAPHIC SEQUENCE	1
7787	7213	SUBSURFACE DRAINAGE	bbfe00ab-ab63-40e0-8752-8f47d17c1d39	EARTH SCIENCE > SOLID EARTH > GEOMORPHIC LANDFORMS/PROCESSES > KARST PROCESSES > KARST HYDROLOGY > SUBSURFACE DRAINAGE	1
7788	7241	TEMPERATURE GRADIENT RATE	f4573e47-3cce-49ec-98d3-b5b3bb51371e	EARTH SCIENCE > SOLID EARTH > GEOTHERMAL DYNAMICS > GEOTHERMAL TEMPERATURE > TEMPERATURE GRADIENT > TEMPERATURE GRADIENT RATE	1
7789	7260	CLEAVAGE	ec950d11-30a8-44c3-b1f3-8e93b131211f	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7790	7260	COLOR	c5bc5153-d8ed-455b-9a05-aebb1026e2fb	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7791	7260	COMPOSITION/TEXTURE	8d396c19-6c45-44f6-9b59-53e1c3712622	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7792	7260	ELECTRICAL	dfb9f260-ce31-4bdc-99af-f3a6f89f52a2	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7793	7260	HARDNESS	26ea8426-2996-4b93-aff2-f3b9cd2f8a7a	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7794	7260	LUMINESCENCE	03939ec7-9310-4440-b761-c8a6b32f1f43	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7795	7260	LUSTER	a4596f71-207c-4037-b3a1-7ab0cd12daec	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7796	7260	REFLECTION	60e242ac-0f08-4574-bf92-b5e6536603cb	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7797	7260	SPECIFIC GRAVITY	2b1b868a-71ff-4a9e-9d32-371a4b91f1a3	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7798	7260	STABILITY	23da8344-174b-4931-b460-9fcfaf824ec9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > GAS HYDRATES > GAS HYDRATES PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7799	7264	CLEAVAGE	746a7f6e-8923-47a1-9e95-9103a1231fc4	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7800	7264	COLOR	7ca1ab0a-2aa1-438c-b4c0-93dd8db37bb1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7801	7264	COMPOSITION/TEXTURE	2cb4e7de-fba7-420a-9137-ac10e298fd63	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7802	7264	ELECTRICAL	8cd774ee-2437-4790-ae2c-4492ecfc5013	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7803	7264	HARDNESS	8443b43e-9512-4389-bc89-11c7510144f6	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7804	7264	LUMINESCENCE	bd075d4b-1112-4290-920d-cf15280d54b8	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7805	7264	LUSTER	e1e3f623-5a18-46a8-b8a8-22c082b643ad	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7806	7264	REFLECTION	19791e07-39bf-4635-b695-a819e38e20ca	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7807	7264	SPECIFIC GRAVITY	ba73a304-0302-40bc-af08-79d923054162	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7808	7264	STABILITY	92b21b46-90e1-4ea6-a5be-e2ce663a028d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > IGNEOUS ROCKS > IGNEOUS ROCK PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7809	7267	CLEAVAGE	37edb662-820e-410f-a45c-7a419bce0c8b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7810	7267	COLOR	a2a5a2e1-6ac8-4bd4-9fe6-00f043bc148b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7811	7267	COMPOSITION/STRUCTURE	1afa91ea-2b60-48d6-b065-093cd20408cd	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/STRUCTURE	1
7812	7267	ELECTRICAL	ebebffc8-474e-46a9-b194-5cfe5a309e88	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7813	7267	HARDNESS	ebc1d1d7-98b7-4448-a6b0-80b15de99259	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7814	7267	LUMINESCENCE	b727b561-f738-436d-bb96-137b455bb54a	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7815	7267	LUSTER	af12ef6b-836b-40bf-959b-ec2d82c87389	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7816	7267	REFLECTION	f9385327-31fe-49a6-b3d6-073d6897ff4a	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7817	7267	SPECIFIC GRAVITY	c3a008a8-0af3-4595-9c32-1fc8bee47c9f	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7818	7267	STABILITY	3ff1adcf-563f-47b3-902e-0231051dc8e7	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METALS > METALS PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7819	7271	CLEAVAGE	f433284b-5def-465b-a532-62f0961294d0	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7820	7271	COLOR	ee3df8b7-0b0b-40ed-b9fa-cc3205d95669	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7821	7271	COMPOSITION/TEXTURE	9dbdb70e-7bea-4473-a7a9-9a7edf843af1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7822	7271	ELECTRICIAL	abd86f50-fc17-4020-a6ac-f0066fc5f7ec	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > ELECTRICIAL	1
7823	7271	HARDNESS	953aecfe-a93d-4994-906f-5a1f8c4baa76	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7824	7271	LUMINESCENCE	f8740a28-ec13-4ce8-8541-2ecae035b297	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7825	7271	LUSTER	93aee4f9-2bcc-4208-b538-0c92f1ac1f42	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7826	7271	REFLECTION	94bc302a-d9ce-4f8f-982b-08a35772e5e9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7827	7271	SPECIFIC GRAVITY	3fa18e78-7b40-425b-8773-ad3f0dab7cf4	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7828	7271	STABILITY	0cbc201c-f58a-44a2-9515-f23eefc9be03	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METAMORPHIC ROCKS > METAMORPHIC ROCK PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7829	7275	CLEAVAGE	d9add64c-1764-4ddb-b088-71c77084a2f5	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7830	7275	COLOR	f54cb873-f20a-4476-835e-fd968c9b1937	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7831	7275	COMPOSITION/STRUCTURE	94370298-393b-4faa-bbb1-f8b6a47b9d56	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/STRUCTURE	1
7832	7275	ELECTRICAL	0de2a94f-9bd1-4ad0-b5b8-4a8237d049bf	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7833	7275	HARDNESS	a2c042a4-2658-48c1-a511-7a5dbff2b63d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7834	7275	LUMINESCENCE	83aff0db-35fd-45f9-b409-692b17941f79	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7835	7275	LUSTER	651a6368-251e-45f6-8496-1f798de85db5	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7836	7275	REFLECTION	547c2bee-40ce-4b23-8338-5fa7c6ad8a8d	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7837	7275	SPECIFIC GRAVITY	7b6d19eb-616b-45cf-a1e6-cc8b549128f1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7838	7275	STABILITY	a1d083b5-3233-4053-a479-4eb7d347c34b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7839	7276	LUSTER	5a8bc1e7-a74d-4acc-9ac2-8fea047068a8	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > METEORITES > METEORITE VERTICAL/GEOGRPAHIC DISTRIBUTION > LUSTER	1
7840	7279	CLEAVAGE	a40aafdc-dcc0-43f0-bc57-3a567631fa3b	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7841	7279	COLOR	d8bea85a-4578-410f-b58a-4927b8963aef	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7842	7279	COMPOSITION/TEXTURE	9d828679-c6d3-4f74-9489-d9688509a025	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7843	7279	ELECTRICAL	a9f3ac40-047e-4649-bf0f-03480d6174ae	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7844	7279	HARDNESS	1545d45e-a4e6-43bd-a3ae-8d3a0a25b41e	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7845	7279	LUMINESCENCE	307f8625-b4cf-4856-9d62-b200e94429a2	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7846	7279	LUSTER	1c44d356-308d-4f92-8fe4-201edff3a02e	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7847	7279	REFLECTION	f2057998-1d06-4e58-9177-447942355d66	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7848	7279	SPECIFIC GRAVITY	cef686dd-4efe-4e4a-b6ef-360879b20dc9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7849	7279	STABILITY	3feb3e65-5a44-46db-ba7b-ceb695e4fb50	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > MINERALS > MINERAL PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7850	7284	CLEAVAGE	6a22f994-b311-4042-b517-35612ccf2bb6	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7851	7284	COLOR	bac88c42-fd8d-4970-878d-441977f00ffc	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7852	7284	COMPOSITION/TEXTURE	f53dd88a-d2a0-4a97-bdcf-70e013461bbe	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7853	7284	ELECTRICAL	ffc61516-ea33-48f3-94df-7065fea388ee	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7854	7284	HARDNESS	70cebb8f-f944-4fe7-be08-1ed86d50eb7c	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7855	7284	LUMINESCENCE	a8f6fca6-7a5e-49f7-9b32-813aaf42d0db	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7856	7284	LUSTER	2e806852-5790-484f-9aee-a7cfc6683ec0	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7857	7284	REFLECTION	9911bf57-9d52-4fb3-a915-9e522e9845d5	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7858	7284	SPECIFIC GRAVITY	42632143-3d8c-40d9-a0ab-9fdffb98a6c9	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7859	7284	STABILITY	07d5a2e4-47ef-4bee-81a7-42ef2eb7a77c	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > NON-METALLIC MINERALS > NON-METALLIC MINERAL PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7860	7289	CLEAVAGE	b5ae8710-8c7e-48ab-bf0f-2f18b2598a5a	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > CLEAVAGE	1
7861	7289	COLOR	e0c40575-4033-4e91-9874-3cd83ce80bc1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > COLOR	1
7862	7289	COMPOSITION/TEXTURE	dbfa6bae-c59a-4c41-b3d1-12b3fd6b5641	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > COMPOSITION/TEXTURE	1
7863	7289	ELECTRICAL	f5cd9ac7-6b10-44dd-8b1d-660a7a681518	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > ELECTRICAL	1
7864	7289	HARDNESS	99d75da3-aa22-4d29-9a56-7e0413665031	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > HARDNESS	1
7865	7289	LUMINESCENCE	3e705ebc-c58f-460d-b5e7-1da05ee45cc1	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > LUMINESCENCE	1
7866	7289	LUSTER	1fca9e52-07fa-424b-b75a-ef1003e77b56	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > LUSTER	1
7867	7289	REFLECTION	73e9349c-08db-4ca5-87f8-bbe785c25629	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > REFLECTION	1
7868	7289	SPECIFIC GRAVITY	383eb3f9-49bb-4210-ab59-030eeb1f68c3	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > SPECIFIC GRAVITY	1
7869	7289	STABILITY	54a4a67a-b1ed-429b-876b-a595164a807c	EARTH SCIENCE > SOLID EARTH > ROCKS/MINERALS/CRYSTALS > SEDIMENTARY ROCKS > SEDIMENTARY ROCK PHYSICAL/OPTICAL PROPERTIES > STABILITY	1
7870	7294	SEISMIC BODY WAVES	f66893ce-3ea6-4c52-bc27-bc322a41b748	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > SEISMIC PROFILE > SEISMIC BODY WAVES	1
7871	7294	SEISMIC SURFACE WAVES	02836842-3d46-46e0-a816-bd2f407f3fb3	EARTH SCIENCE > SOLID EARTH > TECTONICS > EARTHQUAKES > SEISMIC PROFILE > SEISMIC SURFACE WAVES	1
7872	7295	CRUSTAL MOTION DIRECTION	a629b645-2c5f-48d6-8363-71bc636457d6	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > CRUSTAL MOTION > CRUSTAL MOTION DIRECTION	1
7873	7295	CRUSTAL MOTION RATE	88a6ed54-6504-4787-9d98-d511d4f4ae83	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > CRUSTAL MOTION > CRUSTAL MOTION RATE	1
7874	7296	FAULT MOVEMENT DIRECTION	399e5858-8238-451f-8da3-84dc9edfe9a2	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > FAULT MOVEMENT > FAULT MOVEMENT DIRECTION	1
7875	7296	FAULT MOVEMENT RATE	fbbd2aab-73d6-4945-bf1b-c6d543f3f79b	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > FAULT MOVEMENT > FAULT MOVEMENT RATE	1
7876	7298	REBOUND DIRECTION	c185f7f5-0c62-489f-b365-9424e054de58	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > ISOSTATIC REBOUND > REBOUND DIRECTION	1
7877	7298	REBOUND RATE	f0b2ab0f-46eb-426b-924b-471e4d1b7598	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > ISOSTATIC REBOUND > REBOUND RATE	1
7878	7299	PLATE MOTION DIRECTION	03b6b427-6be5-4452-a457-a9ea8c7f0473	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > LITHOSPHERIC PLATE MOTION > PLATE MOTION DIRECTION	1
7879	7299	PLATE MOTION RATE	9cd46f88-24ba-4f2d-96b7-ab5a9333207b	EARTH SCIENCE > SOLID EARTH > TECTONICS > PLATE TECTONICS > LITHOSPHERIC PLATE MOTION > PLATE MOTION RATE	1
7880	7304	ASH/DUST COMPOSITION	372b4016-80ab-4126-b6d1-e847bbf0b44f	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > ASH/DUST COMPOSITION	1
7881	7304	ASH/DUST DISPERSION	89f66579-8de7-4c83-b75f-871bc8d378ac	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > ASH/DUST DISPERSION	1
7882	7304	GAS/AEROSOL COMPOSITION	54b94cdf-b8e2-4c81-b5aa-5652f053244e	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > GAS/AEROSOL COMPOSITION	1
7883	7304	GAS/AEROSOL DISPERSION	b1d60933-636e-48ff-b5a8-43afa60602f3	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > GAS/AEROSOL DISPERSION	1
7884	7304	LAVA COMPOSITION/TEXTURE	0eb6fc71-dfb0-4451-85f7-08ceaf37c552	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > LAVA COMPOSITION/TEXTURE	1
7885	7304	LAVA SPEED/FLOW	9387a7bc-7356-41a5-9682-f5e71da5a858	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > LAVA SPEED/FLOW	1
7886	7304	MAGMA COMPOSITION/TEXTURE	40f0a368-7261-43f7-839c-64e428270442	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > MAGMA COMPOSITION/TEXTURE	1
7887	7304	MAGMA SPEED/FLOW	af04626c-fe27-4ac6-a948-e93debb6c2d6	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > MAGMA SPEED/FLOW	1
7888	7304	PYROCLASTIC PARTICAL SIZE DISTRIBUTION	83cf8358-4fae-4f17-ba02-b8280f2b7209	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > PYROCLASTIC PARTICAL SIZE DISTRIBUTION	1
7889	7304	PYROCLASTICS COMPOSITION/TEXTURE	ab215b31-c540-40c0-9362-3f25ebc148bb	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > PYROCLASTICS COMPOSITION/TEXTURE	1
7890	7304	VOLCANIC EXPLOSIVITY	d9cfb55b-50a2-44f5-b92a-47fe4aadc317	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > VOLCANIC EXPLOSIVITY	1
7891	7304	VOLCANIC GASES	35941db2-59bf-4000-9232-df0beef02da7	EARTH SCIENCE > SOLID EARTH > TECTONICS > VOLCANIC ACTIVITY > ERUPTION DYNAMICS > VOLCANIC GASES	1
7892	7311	WATER TABLE DEPTH	04655f0e-81f1-411c-9cfe-994cd743701e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER FEATURES > WATER TABLE > WATER TABLE DEPTH	1
7893	7312	AQUIFER DEPTH	ee3893bc-f0d6-445a-8982-f852785d5768	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > AQUIFER DEPTH	1
7894	7312	RECHARGE AMOUNT	2cd0b33e-4805-4930-ba84-fef6c625a9b4	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > RECHARGE AMOUNT	1
7895	7312	RECHARGE FREQUENCY	e89dc20d-0570-41ca-8039-38316332238a	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > RECHARGE FREQUENCY	1
7896	7313	DISCHARGE AMOUNT	4f30855f-5bf1-46a8-b2ce-ce2fa00485ec	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISCHARGE > DISCHARGE AMOUNT	1
7897	7313	DISCHARGE RATE	d89d0e4d-0462-43a5-905e-c060db425e7b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISCHARGE > DISCHARGE RATE	1
7898	7314	DISPERSION FREQUENCY	1fa631de-797f-4649-aa26-9f814ddcdb9b	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISPERSION > DISPERSION FREQUENCY	1
7899	7314	DISPERSION RATE	3a95742c-1355-40af-ac86-e24365a67b04	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DISPERSION > DISPERSION RATE	1
7900	7315	DRAINAGE AMOUNT	5ea5be7b-fdbb-4c50-9f54-c0bbd7dcc78c	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DRAINAGE > DRAINAGE AMOUNT	1
7901	7315	DRAINAGE DIRECTION	3045e9ec-ac70-4d72-904a-54094357373a	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > DRAINAGE > DRAINAGE DIRECTION	1
7902	7316	INFILTRATION AMOUNT	59ce52b5-0386-4b51-b5ac-049a0862e9cd	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > INFILTRATION > INFILTRATION AMOUNT	1
7903	7316	INFILTRATION FREQUENCY	55642a14-2ff4-4892-b61a-ae3ece7fbcd7	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > INFILTRATION > INFILTRATION FREQUENCY	1
7904	7316	INFILTRATION RATE	d16cd32f-978d-4ab5-9711-f8189a748399	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > INFILTRATION > INFILTRATION RATE	1
7905	7317	SUBSIDENCE AMOUNT	2922e6fe-3d72-44d3-a972-2e3778194343	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > LAND SUBSIDENCE > SUBSIDENCE AMOUNT	1
7906	7317	SUBSIDENCE RATE	535b876d-9297-49c2-bdcd-4c33e02a47be	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > LAND SUBSIDENCE > SUBSIDENCE RATE	1
7907	7318	PERCOLATION AMOUNT	22566296-aea0-4f01-93c0-fb3256051f27	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > PERCOLATION > PERCOLATION AMOUNT	1
7908	7318	PERCOLATION RATE	acdb39a8-1816-4d8d-bb80-38a94024035e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > PERCOLATION > PERCOLATION RATE	1
7909	7319	INTRUSION AMOUNT	68034344-9c1c-4a5e-a64e-813f6ecf608c	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SALTWATER INTRUSION > INTRUSION AMOUNT	1
7910	7319	INTRUSION RATE	310c5663-1825-46ed-8b64-d1ba7c93ff6d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SALTWATER INTRUSION > INTRUSION RATE	1
7911	7320	AVERAGE FLOW	92bfc132-bc15-4952-99a7-763f109c1e7e	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SUBSURFACE FLOW > AVERAGE FLOW	1
7912	7320	FLOW VELOCITY	dd27825d-7b6e-4a70-9a45-c68d646a1cc5	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SUBSURFACE FLOW > FLOW VELOCITY	1
7913	7320	PEAK FLOW	48f02169-8eab-487d-a24b-4b36ec707b13	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > GROUND WATER > GROUND WATER PROCESSES/MEASUREMENTS > SUBSURFACE FLOW > PEAK FLOW	1
7914	7326	AQUIFER DEPTH	37e1daa7-503a-4d5c-b6d7-c18b71030bc6	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > AQUIFER DEPTH	1
7915	7326	RECHARGE AMOUNT	f9c86356-381e-4f7e-9193-10c274eae41c	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > RECHARGE AMOUNT	1
7916	7326	RECHARGE FREQUENCY	424652b2-92b2-4dee-9f77-016f905b1569	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > AQUIFER RECHARGE > RECHARGE FREQUENCY	1
7917	7327	AVERAGE FLOW	f8f16152-094e-4130-8346-2a9bba5872a0	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DISCHARGE/FLOW > AVERAGE FLOW	1
7918	7327	BASE FLOW	609f7831-5145-4a5c-bd58-d0b426058740	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DISCHARGE/FLOW > BASE FLOW	1
7919	7327	FLOW VELOCITY	f77adcc6-e320-4fd9-80c9-958e75cd46d3	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DISCHARGE/FLOW > FLOW VELOCITY	1
7920	7327	PEAK FLOW	231dd4ab-8b74-45ba-8933-09ab291594ea	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DISCHARGE/FLOW > PEAK FLOW	1
7921	7328	DRAINAGE AMOUNT	71926eb5-b64c-42d9-be6a-26f7b2a5fbf1	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DRAINAGE > DRAINAGE AMOUNT	1
7922	7328	DRAINAGE DIRECTION	97b68ee7-b729-4828-924d-d0758b43d8e9	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > DRAINAGE > DRAINAGE DIRECTION	1
7923	7329	FLOOD FREQUENCY	bf470637-8aea-47a8-b075-40b394303747	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > FLOODS > FLOOD FREQUENCY	1
7924	7329	FLOOD LEVELS	44278367-2c4d-4309-90a2-03244a12ae39	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > FLOODS > FLOOD LEVELS	1
7925	7332	INUNDATION AMOUNT	ae35e34f-92de-4107-b277-abaf7a652f2d	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > INUNDATION > INUNDATION AMOUNT	1
7926	7332	INUNDATION FREQUENCY	3265052b-38e1-472c-ab91-70b39b549854	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > INUNDATION > INUNDATION FREQUENCY	1
7927	7332	INUNDATION LEVEL	5af94668-05f5-41ee-aa65-82dca2a359fc	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > INUNDATION > INUNDATION LEVEL	1
7928	7333	RUNOFF RATE	f54d4750-b9b3-47fa-b56a-a1d57fcbc978	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > RUNOFF > RUNOFF RATE	1
7929	7333	TOTAL RUNOFF	0eb4156f-e4ab-4e02-a473-df4b44290556	EARTH SCIENCE > TERRESTRIAL HYDROSPHERE > SURFACE WATER > SURFACE WATER PROCESSES/MEASUREMENTS > RUNOFF > TOTAL RUNOFF	1
7930	7439	RIMING	889253e1-e189-4f75-bdc7-7e612b19e3ae	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CLOUD MICROPHYSICS > DROPLET GROWTH > ACCRETION > RIMING	1
7931	7444	CUMULONIMBUS INCUS	52f4dfb0-4583-4d82-8cb7-813ffaadd783	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULONIMBUS > CUMULONIMBUS CAPILLATUS > CUMULONIMBUS INCUS	1
7932	7447	TOWERING CUMULUS	79668331-c50d-49da-aea6-83c94545f9e3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS CONGESTUS > TOWERING CUMULUS	1
7933	7448	FAIR WEATHER CUMULUS	ef4de9ce-01ee-4bf0-8814-abefd1bad4b9	EARTH SCIENCE > ATMOSPHERE > CLOUDS > CONVECTIVE CLOUDS/SYSTEMS (OBSERVED/ANALYZED) > CUMULUS > CUMULUS HUMILIS > FAIR WEATHER CUMULUS	1
7934	7460	STRATOCUMULUS CASTELLANUS	53378c8d-0324-4473-8bbd-231aed830d26	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS CUMILIFORMIS > STRATOCUMULUS CASTELLANUS	1
7935	7460	STRATOCUMULUS DIURNALIS	16e33a06-ae4b-48cd-be7f-ad44f3dfd23b	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS CUMILIFORMIS > STRATOCUMULUS DIURNALIS	1
7936	7460	STRATOCUMULUS MAMMATUS	3adff54b-cfc7-4ba0-ba06-7a06b8c4876a	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS CUMILIFORMIS > STRATOCUMULUS MAMMATUS	1
7937	7460	STRATOCUMULUS VESPERALIS	8fc75200-666d-4b59-a493-99e08e55e57d	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS CUMILIFORMIS > STRATOCUMULUS VESPERALIS	1
7938	7461	STRATOCUMULUS LENTICULARIS	12adeea5-f3e7-4f72-a029-f1e52411de18	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS UNDULATAS > STRATOCUMULUS LENTICULARIS	1
7939	7461	STRATOCUMULUS OPACUS	53ade6b0-1b8c-4766-b9c1-4d40d1f69482	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS UNDULATAS > STRATOCUMULUS OPACUS	1
7940	7461	STRATOCUMULUS PERLUCIDUS	94fa2efc-0e7f-4dce-9f2a-0d6f34edcb92	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS UNDULATAS > STRATOCUMULUS PERLUCIDUS	1
7941	7461	STRATOCUMULUS TRANSLUCIDUS	b962de0e-f115-4452-95be-7a4af6687bc3	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/LOW LEVEL CLOUDS (OBSERVED/ANALYZED) > STRATOCUMULUS > STRATOCUMULUS UNDULATAS > STRATOCUMULUS TRANSLUCIDUS	1
7942	7463	LENTICULAR CLOUDS	d5e72d73-22f6-4f4c-b937-b71d84960a1e	EARTH SCIENCE > ATMOSPHERE > CLOUDS > TROPOSPHERIC/MID-LEVEL CLOUDS (OBSERVED/ANALYZED) > ALTOCUMULUS > ALTOCUMULUS LENTICULARIS > LENTICULAR CLOUDS	1
7943	7563	TUNAS AND ALLIES	1369d226-2b9b-4f69-a197-6e24523b21e7	EARTH SCIENCE > BIOLOGICAL CLASSIFICATION > ANIMALS/VERTEBRATES > FISH > RAY-FINNED FISHES > PERCH-LIKE FISHES > TUNAS AND ALLIES	1
7944	7687	CARBON ISOTOPE	437f13e8-0b8a-44a2-a7fd-5b41a00299db	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > TREE RINGS > ISOTOPIC ANALYSIS > CARBON ISOTOPE	1
7945	7687	HYDROGEN ISOTOPE	89387757-3548-4fe0-a383-d8f935f07c71	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > TREE RINGS > ISOTOPIC ANALYSIS > HYDROGEN ISOTOPE	1
7946	7687	OXYGEN ISOTOPE	e91ff41a-5cf5-460b-b765-c553ca2a4ae2	EARTH SCIENCE > CLIMATE INDICATORS > PALEOCLIMATE INDICATORS > BIOLOGICAL RECORDS > TREE RINGS > ISOTOPIC ANALYSIS > OXYGEN ISOTOPE	1
\.


--
-- TOC entry 5662 (class 0 OID 87155)
-- Dependencies: 212
-- Data for Name: licenses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.licenses (id, short_title, title, summary, full_text, link, by_attribution, share_alike, commercial_use) FROM stdin;
4	ODbL	Open Data Commons Open Database License	This record and associated data sets are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/	\N	https://opendatacommons.org/files/2018/02/odbl-10.txt	t	t	t
5	ODC-by	Open Data Commons Attribution License v1.0	This record and associated data sets are made available under the Open Data Commons Attribution License: http://opendatacommons.org/licenses/by/1.0.This data is made available under the Open Data Commons Attribution License: http://opendatacommons.org/licenses/by/1.0	\N	https://opendatacommons.org/files/2018/02/odc_by_1.0_public_text.txt	t	f	t
6	CC BY 4.0	Creative Commons Attribution 4.0 International	You are free to: Share — copy and redistribute the material in any medium or format; Adapt — remix, transform, and build upon the material; for any purpose, even commercially. Under the following terms: Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.  ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.	\N	https://creativecommons.org/licenses/by/4.0/legalcode.txt	t	f	t
7	CC BY-SA 4.0	Creative Commons Attribution-ShareAlike 4.0 International	You are free to: Share — copy and redistribute the material in any medium or format; Adapt — remix, transform, and build upon the material; for any purpose, even commercially. Under the following terms: Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.  ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.	\N	https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt	t	t	t
8	CC BY-NC 4.0	Creative Commons Attribution-NonCommerical 4.0 International	You are free to: Share — copy and redistribute the material in any medium or format Adapt — remix, transform, and build upon the material. Under the following terms: Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.  NonCommercial — You may not use the material for commercial purposes.	\N	https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt 	t	f	f
9	CC BY-NC-SA 4.0	Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International	You are free to: Share — copy and redistribute the material in any medium or format Adapt — remix, transform, and build upon the material. Under the following terms: Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.  NonCommercial — You may not use the material for commercial purposes.  ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.	\N	https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.txt	t	t	f
\.


--
-- TOC entry 5664 (class 0 OID 87166)
-- Dependencies: 214
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.units (id, name, symbol, si) FROM stdin;
1	second	s	s
2	meter	m	m
3	kilogram	kg	kg
4	ampere	A	A
5	kelvin	K	K
6	mole	mol	mol
7	candela	cd	cd
8	radian	rad	1
9	degree	deg	1
10	hertz	Hz	s^-1
11	newton	N	kg*m*s^-2
12	pascal	Pa	kg*m^-1*s^-2
13	joule	J	kg*m^2*s^-2
14	watt	W	kg*m^2*s^-3
15	coulomb	C	s*a
16	volt	V	kg*m^3*s^-3*A^-1
17	farad	F	kg^-1*m^-2*s^4*A^2
18	ohm	ohm	kg*m^2*s^-3*A^-2
19	siemens	S	kg^-1*m^-2*s^3*A^2
20	lux	lx	m^-2*cd
21	relative	-	1
22	mass flux density per hour	cm^3/cm^2h	10^-3*m^3*10^2*m^-2*3600^-1*s*-1
23	hour	h	3600*s
101	degree Celsius	C	K
102	milimeter	10^-3*m	\N
103	mm per day	mm/d	10^-3*m*86400^-1*s^-1
104	hectopascal	10^2*Pa	\N
105	mm per hour	mm/h	10^-3*m*3600^-1*s^-1
106	mm per second	mm/s	10^-3*m**s^-1
107	meter per second	m/s	m*s^-1
108	cubicmeter per second	m3/s	m^3*s^-1
109	liter per second	l/s	10^-3*m^3*s^-1
110	degree	deg.	0.0174533*rad
112	percent	%	10^-2
113	cm3/cm3	cm3/cm3	1
114	kg/kg	kg/kg	1
115	watt per sqauaremeter	W/m2	kg*m^2*s^-3*m^-2
24	megapascal	MPa	10^6*kg*m^-1*s^-2
25	electrical conductivity	EC	S*m^1 -1
\.


--
-- TOC entry 5670 (class 0 OID 87204)
-- Dependencies: 220
-- Data for Name: variables; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.variables (id, name, symbol, unit_id, keyword_id) FROM stdin;
1	air temperature	Ta	101	111
2	soil temperature	Ts	101	5736
3	water temperature	Tw	101	7402
4	discharge	Q	108	7327
5	air pressure	p	104	109
6	relative humidity	RH	112	6308
7	daily rainfall sum	P	103	6434
8	rainfall intensity	Pi	105	6436
9	solar irradiance	SI	115	5236
10	net radiation	Rn	115	5227
11	gravimetric water content	u	114	5727
13	precision	sigma	21	\N
14	sap flow	Fm	22	7424
12	volumetric water content	theta	113	5727
15	matric potential	phi	24	\N
16	bulk electrical conductivity	bEC	25	5111
17	specific electrical conductivity	sEC	25	5111
18	river water level	L	2	\N
\.


--
-- TOC entry 5674 (class 0 OID 87238)
-- Dependencies: 224
-- Data for Name: entries; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.entries (id, title, abstract, external_id, location, geom, version, latest_version_id, comment, license_id, variable_id, datasource_id, embargo, embargo_end, publication, "lastUpdate", is_partial, uuid, citation) FROM stdin;
1	Snow Fall - Hidden Land - Square 22	Snow Fall Square 22- 30mm- east	212	0101000020E610000002452C62D87126406806F1811D0B4A40	\N	1	\N	not yet converted	5	14	1	t	2022-05-18 06:30:14.035695	2020-05-18 06:30:14.035695	2020-07-20 08:59:33.607924	f	3b5fc58b-f221-40e1-8a14-55bbf6e2520d	Maier, W.: Snow Fall - Hidden Land - Square 022, V-FOR-WaTer portal, PERMANENT URI, 2020.
2	Snow Fall - Hidden Land - Square 22	Snow Fall Square 22- 30mm- north-west	214	0101000020E610000002452C62D87126406806F1811D0B4A40	\N	1	\N	not yet converted	5	14	2	t	2022-05-18 06:30:14.560694	2020-05-18 06:30:14.560694	2020-07-20 08:59:33.614265	f	cbd829c8-262a-4d36-a57e-dd4e4d15ed78	Maier, W.: Snow Fall - Hidden Land - Square 022, V-FOR-WaTer portal, PERMANENT URI, 2020.
3	Snow Fall - Hidden Land - Square 29	Snow Fall Square 29- 30mm- north	246	0101000020E610000099F04BFDBC712640761C3F541A0B4A40	\N	1	\N	not yet converted	5	14	3	t	2022-05-18 06:30:14.965695	2020-05-18 06:30:14.965695	2020-07-20 08:59:33.618041	f	cb118f79-b27f-4cf8-ad4e-85406f35d4f6	Maier, W.: Snow Fall - Hidden Land - Square 029, V-FOR-WaTer portal, PERMANENT URI, 2020.
4	Snow Fall - Hidden Land - Square 48	Snow Fall Square 48- 30mm- north 2015	269	0101000020E61000000B24287E8C7126408BA8893E1F0B4A40	\N	1	\N	nan	5	14	4	t	2022-05-18 06:30:15.397694	2020-05-18 06:30:15.397694	2020-07-20 08:59:33.621784	f	4c304dcf-862b-4be8-8d4a-81ceeeeeb43e	Maier, W.: Snow Fall - Hidden Land - Square 048, V-FOR-WaTer portal, PERMANENT URI, 2020.
5	Snow Fall - Hidden Land - Square 50	Snow Fall Square 50- 30mm- east	275	0101000020E61000004A26A77686712640C11DA8531E0B4A40	\N	1	\N	nan	5	14	5	t	2022-05-18 06:30:15.826785	2020-05-18 06:30:15.826785	2020-07-20 08:59:33.62529	f	befeeac4-7741-4b4c-b3e3-6631a536c72a	Maier, W.: Snow Fall - Hidden Land - Square 050, V-FOR-WaTer portal, PERMANENT URI, 2020.
6	Snow Fall - Hidden Land - Square 56	Snow Fall Square 56- 30mm- north	282	0101000020E610000036E50AEF727126403FA7203F1B0B4A40	\N	1	\N	nan	5	14	6	t	2022-05-18 06:30:16.268277	2020-05-18 06:30:16.268277	2020-07-20 08:59:33.628782	f	8bf16112-9c6c-4114-891f-8b337f0debf2	Maier, W.: Snow Fall - Hidden Land - Square 056, V-FOR-WaTer portal, PERMANENT URI, 2020.
7	Snow Fall - Hidden Land - Square 57	Snow Fall Square 57- 30mm- north	292	0101000020E6100000D6743DD1757126409335EA211A0B4A40	\N	1	\N	nan	5	14	7	t	2022-05-18 06:30:16.742299	2020-05-18 06:30:16.742299	2020-07-20 08:59:33.632257	f	40ff6230-de30-4a0d-a0b4-513465d50827	Maier, W.: Snow Fall - Hidden Land - Square 057, V-FOR-WaTer portal, PERMANENT URI, 2020.
8	Snow Fall - Hidden Land - Square 58	Snow Fall Square 58- 30mm- east-north-east	306	0101000020E6100000807EDFBF79712640A46C91B41B0B4A40	\N	1	\N	nan	5	14	8	t	2022-05-18 06:30:17.227577	2020-05-18 06:30:17.227577	2020-07-20 08:59:33.63576	f	907e1f63-2986-43de-98a9-b15b4f21cacb	Maier, W.: Snow Fall - Hidden Land - Square 058, V-FOR-WaTer portal, PERMANENT URI, 2020.
9	Snow Fall - Hidden Land - Square 06	Snow Fall Square 06 - 30mm - east - commertial	326	0101000020E6100000B79C4B7155712640A87004A9140B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	9	t	2022-05-18 06:30:17.753487	2020-05-18 06:30:17.753487	2020-07-20 08:59:33.639265	f	ace322a6-2649-4e04-b856-a74b897b3cb4	Maier, W.: Snow Fall - Hidden Land - Square 106, V-FOR-WaTer portal, PERMANENT URI, 2020.
10	Snow Fall - Hidden Land - Square 08	Snow Fall Square 08 - 30mm - east-north-east - commertial	333	0101000020E61000003C855CA967712640D828EB37130B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	10	t	2022-05-18 06:30:18.202247	2020-05-18 06:30:18.202247	2020-07-20 08:59:33.642779	f	543e9ad0-19e5-4542-aeaf-635cc1ea831e	Maier, W.: Snow Fall - Hidden Land - Square 108, V-FOR-WaTer portal, PERMANENT URI, 2020.
11	Snow Fall - Hidden Land - Square 14	Snow Fall Square 14 - 30mm - north - commertial	347	0101000020E6100000E1D1C6116B712640286211C30E0B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	11	t	2022-05-18 06:30:18.673814	2020-05-18 06:30:18.673814	2020-07-20 08:59:33.646328	f	90b90d5a-ac6a-43b1-a2d7-a4526b0eb877	Maier, W.: Snow Fall - Hidden Land - Square 114, V-FOR-WaTer portal, PERMANENT URI, 2020.
12	Snow Fall - Hidden Land - Square 43	Snow Fall Square 43 - 30mm - north - commertial	361	0101000020E6100000395E81E849712640286211C30E0B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	12	t	2022-05-18 06:30:19.11864	2020-05-18 06:30:19.11864	2020-07-20 08:59:33.64984	f	ca4216e2-2a66-4ad3-b924-21be5482d92a	Maier, W.: Snow Fall - Hidden Land - Square 143, V-FOR-WaTer portal, PERMANENT URI, 2020.
13	Snow Fall - Hidden Land - Square 58	Snow Fall Square 58 - 30mm - east-north-east - commertial	373	0101000020E6100000AEB8382A37712640D07EA4880C0B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	13	t	2022-05-18 06:30:19.592477	2020-05-18 06:30:19.592477	2020-07-20 08:59:33.73594	f	31714aea-9bdc-4f44-abaa-83cf51af7744	Maier, W.: Snow Fall - Hidden Land - Square 158, V-FOR-WaTer portal, PERMANENT URI, 2020.
14	Snow Fall - Hidden Land - Square 85	Snow Fall Square 85 - 10mm - ene	380	0101000020E6100000BC24CE8AA8712640A6B73F170D0B4A40	\N	1	\N	nan	5	14	14	t	2022-05-18 06:30:20.04366	2020-05-18 06:30:20.044636	2020-07-20 08:59:33.739772	f	97e1979e-7512-436f-88b3-76fb5b3f9a8a	Maier, W.: Snow Fall - Hidden Land - Square 185, V-FOR-WaTer portal, PERMANENT URI, 2020.
15	Snow Fall - Hidden Land - Square 18	Snow Fall Square 18- 30mm- east	447	0101000020E61000006C257497C47126405516855D140B4A40	\N	1	\N	not yet converted	5	14	15	t	2022-05-18 06:30:20.518116	2020-05-18 06:30:20.518116	2020-07-20 08:59:33.743561	f	48bb0536-21a5-4144-8124-2463397479d4	Maier, W.: Snow Fall - Hidden Land - Square 218, V-FOR-WaTer portal, PERMANENT URI, 2020.
16	Snow Fall - Hidden Land - Square 18	Snow Fall Square 18- 30mm- north	448	0101000020E61000006C257497C47126405516855D140B4A40	\N	1	\N	not yet converted	5	14	16	t	2022-05-18 06:30:20.967097	2020-05-18 06:30:20.967097	2020-07-20 08:59:33.747519	f	22dec20b-adb0-4197-a7aa-594a11c71d4c	Maier, W.: Snow Fall - Hidden Land - Square 218, V-FOR-WaTer portal, PERMANENT URI, 2020.
17	Snow Fall - Hidden Land - Square 82	Snow Fall Square 82 - 30mm - north - commertial	465	0101000020E6100000B96C74CE4F712640454772F90F0B4A40	\N	1	\N	commertial sensor in 30mm depth	5	14	17	t	2022-05-18 06:30:21.47477	2020-05-18 06:30:21.47477	2020-07-20 08:59:33.751412	f	14d6d958-c6f4-4761-a664-f1f5e9434088	Maier, W.: Snow Fall - Hidden Land - Square 282, V-FOR-WaTer portal, PERMANENT URI, 2020.
19	test Sensor North	\N	10350083	0101000020E6100000EA95B20C716C1F4094BC3AC780024840	\N	1	\N	\N	4	1	18	f	2022-11-02 12:24:42.608795	2020-11-02 12:24:42.60885	2020-11-02 12:25:03.09644	f	b9f2e57f-7daa-43d5-b86c-171c2238a1b5	\N
18	test Sensor South	\N	10350083	0101000020E6100000CEAACFD5566C1F4001DBC1887D024840	\N	1	\N	\N	4	1	19	f	2022-11-02 12:24:42.483029	2020-11-02 12:24:42.483112	2020-11-02 12:25:03.202206	f	a35c3c50-a070-42bc-ba5c-acda212bbc7b	\N
\.


--
-- TOC entry 5729 (class 0 OID 134240)
-- Dependencies: 289
-- Data for Name: author_manage_resource; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_resource (id, type, link, "dataEntry_id") FROM stdin;
22	timeseries	/	17
23	timeseries	/	16
24	timeseries	/	15
25	timeseries	/	14
26	timeseries	/	13
27	timeseries	/	12
\.


--
-- TOC entry 5737 (class 0 OID 134274)
-- Dependencies: 297
-- Data for Name: author_manage_accessrequest; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_accessrequest (id, "creationDate", description, resource_id, sender_id) FROM stdin;
1	2021-02-04 09:02:49.11413+01		22	5
\.


--
-- TOC entry 5735 (class 0 OID 134264)
-- Dependencies: 295
-- Data for Name: author_manage_deletionrequest; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_deletionrequest (id, "creationDate", description, resource_id, sender_id) FROM stdin;
\.


--
-- TOC entry 5658 (class 0 OID 87133)
-- Dependencies: 208
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.persons (id, first_name, last_name, affiliation, organisation_name, attribution, is_organisation, organisation_abbrev) FROM stdin;
1	Walter	Maier	University for Computational Snowfall, Hardwork Group	Top Center TC	\N	f	\N
2	Peter, P.	Paulsen	\N	\N	\N	f	\N
\.


--
-- TOC entry 5727 (class 0 OID 134230)
-- Dependencies: 287
-- Data for Name: author_manage_profile; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_profile (id, "checkedAssociation", "metacatalogPerson_id", user_id) FROM stdin;
24	t	\N	3
25	t	\N	5
26	t	\N	4
\.


--
-- TOC entry 5733 (class 0 OID 134256)
-- Dependencies: 293
-- Data for Name: author_manage_resource_maintainers; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_resource_maintainers (id, resource_id, maintainer_id) FROM stdin;
1	27	2
\.


--
-- TOC entry 5739 (class 0 OID 134284)
-- Dependencies: 299
-- Data for Name: author_manage_resource_owners; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_resource_owners (id, resource_id, owner_id) FROM stdin;
13	22	2
14	23	2
15	24	2
\.


--
-- TOC entry 5731 (class 0 OID 134248)
-- Dependencies: 291
-- Data for Name: author_manage_resource_readers; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.author_manage_resource_readers (id, resource_id, customuser_id) FROM stdin;
5	25	2
6	26	2
\.


--
-- TOC entry 5677 (class 0 OID 87286)
-- Dependencies: 227
-- Data for Name: details; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.details (id, entry_id, key, stem, value, description, thesaurus_id) FROM stdin;
1	1	height	height	1.3	\N	\N
2	1	dbh	dbh	53.04	\N	\N
3	1	depth	depth	30mm	\N	\N
4	1	species	speci	fern	\N	\N
5	2	height	height	1.3	\N	\N
6	2	dbh	dbh	53.04	\N	\N
7	2	depth	depth	30mm	\N	\N
8	2	species	speci	fern	\N	\N
9	3	height	height	1.3	\N	\N
10	3	dbh	dbh	22.07	\N	\N
11	3	depth	depth	30mm	\N	\N
12	3	species	speci	salt	\N	\N
13	4	height	height	1.3	\N	\N
14	4	dbh	dbh	17.91	\N	\N
15	4	depth	depth	30mm	\N	\N
16	4	species	speci	salt	\N	\N
17	5	height	height	1.3	\N	\N
18	5	dbh	dbh	62.47	\N	\N
19	5	depth	depth	30mm	\N	\N
20	5	species	speci	fern	\N	\N
21	6	height	height	1.3	\N	\N
22	6	dbh	dbh	17.64	\N	\N
23	6	depth	depth	30mm	\N	\N
24	6	species	speci	salt	\N	\N
25	7	height	height	1.3	\N	\N
26	7	dbh	dbh	53.78	\N	\N
27	7	depth	depth	30mm	\N	\N
28	7	species	speci	lila	\N	\N
29	8	height	height	1.3	\N	\N
30	8	dbh	dbh	nan	\N	\N
31	8	depth	depth	30mm	\N	\N
32	8	species	speci	lila	\N	\N
33	9	height	height	1.3	\N	\N
34	9	dbh	dbh	46.87	\N	\N
35	9	depth	depth	30mm	\N	\N
36	9	species	speci	lila	\N	\N
37	10	height	height	1.3	\N	\N
38	10	dbh	dbh	89.22	\N	\N
39	10	depth	depth	30mm	\N	\N
40	10	species	speci	lila	\N	\N
41	11	height	height	1.3	\N	\N
42	11	dbh	dbh	20.06	\N	\N
43	11	depth	depth	30mm	\N	\N
44	11	species	speci	salt	\N	\N
45	12	height	height	1.3	\N	\N
46	12	dbh	dbh	61.5	\N	\N
47	12	depth	depth	30mm	\N	\N
48	12	species	speci	lila	\N	\N
49	13	height	height	1.3	\N	\N
50	13	dbh	dbh	23.2	\N	\N
51	13	depth	depth	30mm	\N	\N
52	13	species	speci	lila	\N	\N
53	14	height	height	1.3	\N	\N
54	14	dbh	dbh	33.1	\N	\N
55	14	depth	depth	10mm	\N	\N
56	14	species	speci	fern	\N	\N
57	15	height	height	1.3	\N	\N
58	15	dbh	dbh	56.67	\N	\N
59	15	depth	depth	30mm	\N	\N
60	15	species	speci	fern	\N	\N
61	16	height	height	1.3	\N	\N
62	16	dbh	dbh	56.67	\N	\N
63	16	depth	depth	30mm	\N	\N
64	16	species	speci	fern	\N	\N
65	17	height	height	1.3	\N	\N
66	17	dbh	dbh	50.31	\N	\N
67	17	depth	depth	30mm	\N	\N
68	17	species	speci	lila	\N	\N
69	18	sensor_precision	sensor_precis	0.5	\N	\N
70	19	sensor_precision	sensor_precis	0.5	\N	\N
\.


--
-- TOC entry 5725 (class 0 OID 134197)
-- Dependencies: 285
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 5709 (class 0 OID 134044)
-- Dependencies: 269
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-10-06 13:46:10.339294+02
2	auth	0001_initial	2020-10-06 13:46:34.668039+02
3	admin	0001_initial	2020-10-06 13:46:35.338722+02
4	admin	0002_logentry_remove_auto_add	2020-10-06 13:46:35.44667+02
5	admin	0003_logentry_add_action_flag_choices	2020-10-06 13:46:35.470898+02
6	contenttypes	0002_remove_content_type_name	2020-10-06 13:46:35.516058+02
7	auth	0002_alter_permission_name_max_length	2020-10-06 13:46:35.537327+02
8	auth	0003_alter_user_email_max_length	2020-10-06 13:46:35.57139+02
9	auth	0004_alter_user_username_opts	2020-10-06 13:46:35.597666+02
10	auth	0005_alter_user_last_login_null	2020-10-06 13:46:35.623866+02
11	auth	0006_require_contenttypes_0002	2020-10-06 13:46:35.637998+02
12	auth	0007_alter_validators_add_error_messages	2020-10-06 13:46:35.66764+02
13	auth	0008_alter_user_username_max_length	2020-10-06 13:46:35.712713+02
14	auth	0009_alter_user_last_name_max_length	2020-10-06 13:46:35.739152+02
15	auth	0010_alter_group_name_max_length	2020-10-06 13:46:35.764807+02
16	auth	0011_update_proxy_permissions	2020-10-06 13:46:35.795112+02
17	vfw_home	0001_initial	2020-10-06 13:46:35.892931+02
18	author_manage	0001_initial	2020-10-06 13:46:36.200397+02
19	sessions	0001_initial	2020-10-06 13:46:36.993004+02
20	wps_gui	0001_initial	2020-10-06 13:57:37.292586+02
\.


--
-- TOC entry 5740 (class 0 OID 134375)
-- Dependencies: 300
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
gl75sp2bmdkwv4ycozbwzkleys7yky9j	NTgxMDJkMDY2OGIwZDM3MDFlY2UyOWRmM2ZkN2E2NDNjOGZmZTY1NDp7ImRhdGFzZXRzIjpbXX0=	2020-12-22 17:12:14.18901+01
\.


--
-- TOC entry 5654 (class 0 OID 87104)
-- Dependencies: 204
-- Data for Name: entrygroup_types; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.entrygroup_types (id, name, description) FROM stdin;
1	Project	A Project groups datasets into a lager collection of datasets that have been collected or used in the same Campaign.
2	Composite	A composite dataset groups a number of datasets that are inseparable.
\.


--
-- TOC entry 5668 (class 0 OID 87188)
-- Dependencies: 218
-- Data for Name: entrygroups; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.entrygroups (id, type_id, title, description, uuid, publication, "lastUpdate") FROM stdin;
\.


--
-- TOC entry 5682 (class 0 OID 87366)
-- Dependencies: 232
-- Data for Name: generic_1d_data; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.generic_1d_data (entry_id, index, value, "precision") FROM stdin;
\.


--
-- TOC entry 5683 (class 0 OID 87379)
-- Dependencies: 233
-- Data for Name: generic_2d_data; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.generic_2d_data (entry_id, index, value1, value2, precision1, precision2) FROM stdin;
\.


--
-- TOC entry 5685 (class 0 OID 87406)
-- Dependencies: 235
-- Data for Name: generic_geometry_data; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.generic_geometry_data (entry_id, index, geom, srid) FROM stdin;
\.


--
-- TOC entry 5684 (class 0 OID 87392)
-- Dependencies: 234
-- Data for Name: geom_timeseries; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.geom_timeseries (entry_id, tstamp, geom, srid) FROM stdin;
\.


--
-- TOC entry 5700 (class 0 OID 133396)
-- Dependencies: 260
-- Data for Name: heron_upload_uploadedfile; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.heron_upload_uploadedfile (id, title, file, uploaded_at) FROM stdin;
\.


--
-- TOC entry 5696 (class 0 OID 87544)
-- Dependencies: 246
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.logs (id, tstamp, code, description, migration_head) FROM stdin;
1	2020-07-13 07:57:12.726564	5	Database was created in metacatalog < 0.2 version.	1
2	2020-07-13 07:57:12.72768	1	Migrated database to 1 using metacatalog==0.2.0	1
3	2020-12-03 14:05:23.274889	1	Migrated database to 2 using metacatalog==0.2.5	2
\.


--
-- TOC entry 5675 (class 0 OID 87269)
-- Dependencies: 225
-- Data for Name: nm_entrygroups; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.nm_entrygroups (entry_id, group_id) FROM stdin;
\.


--
-- TOC entry 5678 (class 0 OID 87302)
-- Dependencies: 228
-- Data for Name: nm_keywords_entries; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.nm_keywords_entries (keyword_id, entry_id) FROM stdin;
\.


--
-- TOC entry 5660 (class 0 OID 87144)
-- Dependencies: 210
-- Data for Name: person_roles; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.person_roles (id, name, description) FROM stdin;
1	author	the individual or organization whose name should appear first in the citation for the resource (for names that come after the first use co-author). while it is possible to have an author and principle investigator be the same individual or organization, author is not the same as nor synonymous with principle investigator. applicable mainly to documents, reports, memos, etc.
2	custodian	the individual or organization that has accountability and responsibility for the data and ensures appropriate care and maintenance of the resource.
3	distributor	the individual or organization that has accountability and responsibility for the data and ensures appropriate care and maintenance of the resource.
4	originator	the name of the individual or organization who is responsible for the data at the point when the data was first created. applicable for data sets that are an aggregation of two or more data sets or if the data set is the first instance of the signal having been converted into data.
5	owner	the individual or organization that has ownership of the resource.
6	pointOfContact	the individual or organization who is responsible for the initial triage of and answering questions related to the resource.
7	principalInvestigator	the individual or individuals who are the lead researchers for a grant (i.e. head of the laboratory, research group leader, etc.). if there are co-principal investigators then this field will repeat for each principle investigator. while it is possible to have a principal investigator and author be the same individual or organization, principal investigator is not the same nor synonymous with author.
8	processor	the name of the individual or organization who has processed the data in a manner such that the resource has been modified.
9	publisher	the individual or organization who prepares and issues the resource.
10	resourceProvider	the individual or organization that supplies or allocates the resource for another entity.
11	sponsor	the individual or organization who is providing sponsorship for the resource.
12	user	the individuals or organizations who are the intended consumers of the resource.
13	coAuthor	the individual(s) or organization(s) who name(s) should appear after the first name in a citation for the resource (use author to denote the first name in the citation). while it is possible to have a co-author and principal investigator/collaborator be the same individual or organization, co-author is no the same as nor synonymous with principle investigator or collaborator
14	collaborator	party who assists with the generation of the resource other than the principal investigator
15	contributor	the individuals or organizations whose contributions deserve recognition in the citation. contributor is mutually exclusive from author, co-author, principal investigator, and collaborator. use ISO MD_Identification credit field to identify individual or organizations that should be given acknowledgement only.
16	editor	the individual who has made a corrective or editorial change to the resource as part of a systematic revision process.
17	funder	the individual or organization which has provided all or part of the finances associated with the resource.
18	mediator	a class of entity that mediates access to the resource and for whom the resource is intended or useful
19	rightsHolder	he individual or organization who has ownership of the legal right to the resource.
20	stakeholder	an individual or organization who has an interest in the resource and/or is affected by or affects the actions of the resource
\.


--
-- TOC entry 5679 (class 0 OID 87320)
-- Dependencies: 229
-- Data for Name: nm_persons_entries; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.nm_persons_entries (person_id, entry_id, relationship_type_id, "order") FROM stdin;
1	1	1	1
1	2	1	1
1	3	1	1
1	4	1	1
1	5	1	1
1	6	1	1
1	7	1	1
1	8	1	1
1	9	1	1
1	10	1	1
1	11	1	1
1	12	1	1
1	13	1	1
1	14	1	1
1	15	1	1
1	16	1	1
1	17	1	1
2	18	1	1
2	19	1	1
\.


--
-- TOC entry 5258 (class 0 OID 86492)
-- Dependencies: 199
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- TOC entry 5680 (class 0 OID 87340)
-- Dependencies: 230
-- Data for Name: timeseries; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.timeseries (entry_id, tstamp, value, "precision") FROM stdin;
1	2011-11-11 11:11:11	0.11	\N
1	2011-11-11 11:11:16	0.21	\N
1	2011-11-11 11:11:21	0.414	\N
1	2011-11-11 11:11:26	0.31	\N
1	2011-11-11 11:11:41	0.591	\N
1	2011-11-11 11:11:51	0.11	\N
1	2011-11-11 11:11:56	0.2	\N
2	2015-05-07 15:40:00	0.6	\N
2	2015-05-07 15:50:00	0.5	\N
2	2015-05-07 16:00:00	0.5	\N
2	2015-05-07 16:10:00	0.35	\N
2	2015-05-07 16:20:00	0.32	\N
2	2015-08-30 10:20:00	0.33	\N
2	2015-08-30 10:30:00	0.60	\N
2	2015-08-30 10:40:00	0.565	\N
3	2015-04-22 20:10:00	0.1	\N
3	2015-11-01 11:40:00	0.0	\N
3	2015-11-01 11:50:00	0.05	\N
3	2015-11-01 12:00:00	0.460	\N
3	2015-11-01 12:10:00	0.54980	\N
3	2015-11-01 12:20:00	0.310	\N
3	2015-11-01 12:30:00	0.180	\N
3	2015-11-01 12:40:00	0.049	\N
3	2015-11-01 12:50:00	0.2	\N
3	2015-11-01 13:00:00	0.01	\N
4	2015-10-23 10:20:00	0.001	\N
4	2015-11-03 12:50:00	0.21	\N
4	2015-11-03 13:00:00	0.12	\N
4	2015-11-03 13:10:00	0.16836	\N
4	2015-11-03 13:20:00	0.107	\N
4	2015-11-03 13:30:00	0.9943	\N
4	2015-11-03 13:40:00	0.939	\N
4	2015-11-03 13:50:00	0.90002	\N
5	2015-08-18 10:20:00	0.0	\N
5	2015-07-18 10:10:00	0.8799	\N
5	2015-08-19 10:20:00	1.50001	\N
5	2015-08-19 10:30:00	2.8157	\N
5	2015-08-19 10:40:00	1.9051	\N
5	2015-08-19 10:50:00	2.051	\N
5	2015-08-19 11:00:00	0.45458	\N
5	2015-08-19 11:20:00	0.188	\N
5	2015-08-19 11:30:00	0.159987	\N
5	2015-08-19 11:40:00	1.05	\N
6	2015-10-10 18:00:00	0.2662	\N
6	2015-10-10 18:20:00	0.62	\N
6	2015-10-10 18:40:00	0.66	\N
6	2015-10-10 19:00:00	1.2	\N
6	2015-10-11 17:20:00	0.0061	\N
6	2015-10-11 17:40:00	0.739	\N
6	2015-10-11 18:00:00	1.3	\N
6	2015-10-11 18:20:00	0.9	\N
7	2015-04-22 22:05:00	0.5	\N
7	2015-04-22 22:10:00	0.1	\N
7	2015-04-22 22:15:00	0.05	\N
7	2015-04-22 22:20:00	1.0	\N
7	2015-04-22 22:25:00	1.5	\N
7	2015-04-22 22:30:00	2.2	\N
7	2015-04-22 22:35:00	0.8	\N
7	2015-04-22 22:40:00	0.8	\N
7	2015-04-22 22:45:00	0.5465	\N
7	2015-04-22 22:50:00	0.44585	\N
7	2015-04-22 22:55:00	0.87895	\N
8	2015-04-26 07:40:00	0.887987	\N
9	2015-04-30 06:10:00	0.54	\N
9	2015-04-30 06:20:00	0.45	\N
9	2015-04-30 06:30:00	0.12387	\N
9	2015-04-30 06:40:00	0.87897946	\N
9	2015-04-30 06:50:00	0.53218	\N
9	2015-04-30 07:00:00	0.54008	\N
9	2015-04-30 07:10:00	0.08789	\N
9	2015-04-30 07:20:00	0.875	\N
9	2015-04-30 07:30:00	0.84981	\N
9	2015-04-30 07:40:00	0.2389	\N
9	2015-04-30 07:50:00	0.875305	\N
10	2015-04-26 08:00:00	0.01	\N
10	2015-04-26 08:10:00	0.807	\N
10	2015-04-26 08:20:00	0.89508	\N
10	2015-04-26 08:30:00	0.454897	\N
10	2015-04-26 08:40:00	0.08788	\N
10	2015-04-26 08:50:00	0.189987	\N
10	2015-04-26 09:00:00	0.78412	\N
10	2015-04-26 09:20:00	0.022575	\N
10	2015-04-26 09:30:00	0.00416282	\N
10	2015-04-26 09:40:00	0.78942	\N
10	2015-04-26 09:50:00	0.0048	\N
10	2015-04-26 10:30:00	0.0	\N
11	2015-04-26 15:20:00	0.875	\N
11	2015-04-26 15:30:00	0.487	\N
11	2015-04-26 15:40:00	0.875	\N
11	2015-04-26 15:50:00	0.0	\N
11	2015-04-26 16:00:00	0.9870	\N
11	2015-04-26 16:10:00	0.170	\N
11	2015-04-26 16:20:00	0.0848	\N
11	2015-04-26 16:30:00	0.44840	\N
11	2015-04-26 16:40:00	0.01448	\N
11	2015-04-26 16:50:00	0.0488	\N
12	2015-11-05 07:30:00	0.48754	\N
12	2015-11-05 07:40:00	0.78	\N
12	2015-11-05 11:40:00	1.4897	\N
12	2015-11-05 11:50:00	0.947	\N
12	2015-11-05 12:00:00	0.04984	\N
12	2015-11-05 12:10:00	0.0	\N
12	2015-11-05 12:20:00	0.4987	\N
12	2015-11-05 12:30:00	0.137	\N
12	2015-11-05 12:40:00	0.641	\N
12	2015-11-05 12:50:00	0.59	\N
13	2015-08-11 14:50:00	0.15408	\N
13	2015-08-11 15:00:00	0.0844654	\N
13	2015-08-12 00:30:00	0.1650	\N
13	2015-08-12 00:40:00	0.054	\N
13	2015-08-12 00:50:00	0.057	\N
13	2015-08-12 01:00:00	0.087	\N
13	2015-08-12 01:10:00	0.0178	\N
13	2015-08-12 01:20:00	0.0756	\N
13	2015-08-12 01:30:00	0.0544	\N
13	2015-08-12 01:40:00	0.046	\N
13	2015-08-12 01:50:00	0.110	\N
13	2015-08-12 02:00:00	0.0489	\N
13	2015-08-12 02:10:00	0.84650	\N
13	2015-08-12 02:20:00	0.4840	\N
13	2015-08-12 02:30:00	0.8460	\N
13	2015-08-12 02:40:00	0.4840	\N
13	2015-08-12 02:50:00	0.0987	\N
13	2015-08-12 03:00:00	0.4810	\N
13	2015-08-12 03:10:00	0.87540	\N
13	2015-08-12 03:20:00	0.84650	\N
13	2015-08-12 03:30:00	0.84560	\N
13	2015-08-12 03:40:00	0.404890	\N
13	2015-08-12 03:50:00	0.8400	\N
13	2015-08-12 04:00:00	0.49	\N
13	2015-08-12 04:10:00	0.05491	\N
13	2015-08-12 04:20:00	0.0188	\N
13	2015-08-12 04:30:00	0.087114	\N
13	2015-08-12 04:40:00	0.04981	\N
13	2015-08-12 04:50:00	0.11560	\N
13	2015-08-12 05:00:00	0.0	\N
13	2015-08-12 05:10:00	0.0	\N
13	2015-08-12 05:20:00	0.1410	\N
13	2015-08-12 05:30:00	0.1510	\N
13	2015-08-12 05:40:00	0.01898	\N
14	2015-04-28 04:20:00	0.489408	\N
14	2015-04-28 04:30:00	0.048948	\N
14	2015-04-28 04:40:00	0.4770	\N
14	2015-04-28 04:50:00	0.87854	\N
14	2015-04-28 05:00:00	0.54980	\N
14	2015-04-28 05:10:00	0.4856	\N
14	2015-04-28 05:20:00	0.878754	\N
14	2015-04-28 05:30:00	0.37894	\N
14	2015-04-28 05:40:00	0.37484	\N
14	2015-04-28 05:50:00	0.7565	\N
14	2015-04-28 06:00:00	0.49875	\N
14	2015-04-28 06:20:00	0.4887	\N
14	2015-04-28 06:30:00	0.7541	\N
14	2015-04-28 06:40:00	0.64546	\N
15	2015-04-27 10:00:00	1.1	\N
15	2015-04-27 10:10:00	1.0	\N
15	2015-04-27 10:20:00	0.0	\N
15	2015-04-27 10:30:00	0.0	\N
15	2015-04-27 10:40:00	0.0	\N
15	2015-04-27 10:50:00	0.201	\N
15	2015-05-02 14:30:00	0.5049	\N
15	2015-05-02 14:40:00	0.50487	\N
15	2015-05-02 14:50:00	0.59721	\N
15	2015-05-02 15:00:00	0.67891	\N
15	2015-05-02 15:10:00	0.7151	\N
15	2015-05-02 15:20:00	0.451961	\N
15	2015-05-02 15:30:00	0.34984	\N
15	2015-05-02 15:40:00	0.1894	\N
15	2015-05-02 15:50:00	0.07984	\N
15	2015-05-02 16:00:00	0.2484	\N
15	2015-05-02 16:10:00	0.0871	\N
15	2015-05-02 16:20:00	0.0088	\N
15	2015-05-02 16:30:00	0.1974	\N
16	2015-04-23 11:00:00	0.29	\N
16	2015-04-23 11:10:00	0.245649	\N
16	2015-04-23 11:20:00	0.49829	\N
16	2015-04-23 11:30:00	0.5418	\N
16	2015-04-23 11:40:00	0.4551	\N
16	2015-04-23 11:50:00	0.3498	\N
16	2015-04-23 12:00:00	0.2188	\N
16	2015-04-23 12:10:00	0.2184	\N
16	2015-04-23 12:20:00	0.287	\N
16	2015-04-23 12:30:00	0.3789	\N
16	2015-04-23 12:40:00	0.5897	\N
16	2015-04-23 12:50:00	0.68856	\N
16	2015-04-23 13:00:00	0.75156	\N
16	2015-04-23 13:10:00	0.548489	\N
16	2015-04-23 13:20:00	0.6784	\N
16	2015-04-23 13:30:00	0.78654	\N
16	2015-04-23 13:40:00	0.85419	\N
16	2015-04-23 13:50:00	0.5454	\N
17	2015-04-30 22:00:00	0.57815	\N
17	2015-04-30 22:10:00	0.5451	\N
17	2015-04-30 22:20:00	0.587856	\N
17	2015-04-30 22:30:00	0.678915	\N
17	2015-04-30 22:40:00	0.67481	\N
17	2015-04-30 22:50:00	0.7548	\N
17	2015-04-30 23:00:00	0.67551	\N
17	2015-04-30 23:10:00	0.5784654	\N
17	2015-04-30 23:20:00	0.61898	\N
17	2015-04-30 23:30:00	0.6748	\N
17	2015-04-30 23:40:00	0.084564	\N
17	2015-04-30 23:50:00	0.048978	\N
18	2017-12-22 10:55:00	6.54897	\N
18	2017-12-22 11:00:00	5.49845	\N
18	2017-12-22 11:05:00	5.415	\N
18	2017-12-22 11:10:00	2.112	\N
18	2017-12-22 11:15:00	4.211	\N
18	2017-12-22 11:20:00	3.512	\N
18	2017-12-22 11:25:00	4.85645	\N
18	2017-12-22 11:30:00	5.84	\N
18	2017-12-22 11:35:00	5.4184	\N
18	2017-12-22 11:45:00	5.54561	\N
18	2017-12-22 11:55:00	5.512	\N
18	2017-12-22 12:05:00	5.16515	\N
18	2017-12-22 12:15:00	5.010	\N
18	2017-12-22 12:25:00	4.9419084	\N
18	2017-12-22 12:35:00	4.8454	\N
19	2017-12-19 08:35:00	8.711	0.4513228
19	2017-12-19 08:45:00	2.5754	0.054811
19	2017-12-19 09:15:00	5.545	0.0545
19	2017-12-19 09:25:00	6.48944	0.150
19	2017-12-19 09:35:00	1.5481	0.170
19	2017-12-19 09:45:00	6.5166	0.0848
19	2017-12-19 09:55:00	5.5412	0.855
19	2017-12-19 10:05:00	5.24	0.878
19	2017-12-19 10:15:00	5.241	0.788
19	2017-12-19 10:25:00	6.2187	0.878
19	2017-12-19 10:35:00	6.67	0.5897
19	2017-12-19 10:45:00	7.677799	0.40
19	2017-12-19 10:55:00	7.98754	0.40
\.


--
-- TOC entry 5681 (class 0 OID 87353)
-- Dependencies: 231
-- Data for Name: timeseries_2d; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.timeseries_2d (entry_id, tstamp, value1, value2, precision1, precision2) FROM stdin;
\.


--
-- TOC entry 5702 (class 0 OID 133533)
-- Dependencies: 262
-- Data for Name: upload_temp; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.upload_temp (tstamp, value, meta_id) FROM stdin;
\.


--
-- TOC entry 5703 (class 0 OID 133551)
-- Dependencies: 263
-- Data for Name: watts_rsp_authfailureresponse; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.watts_rsp_authfailureresponse (id, watts_ref, "time", msg) FROM stdin;
\.


--
-- TOC entry 5705 (class 0 OID 133559)
-- Dependencies: 265
-- Data for Name: watts_rsp_authsuccessresponse; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.watts_rsp_authsuccessresponse (id, watts_ref, "time", user_id) FROM stdin;
16	e7gZNy1yHFhjBjr615xryY48p5VSe8i3	2020-04-16 11:00:11.036854+02	5
\.


--
-- TOC entry 5707 (class 0 OID 133564)
-- Dependencies: 267
-- Data for Name: watts_rsp_rsakey; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.watts_rsp_rsakey (key_id, intended_usage, sha_size, pem) FROM stdin;
oD5hsP2JmVnTuppZfhLX3rSGQInpD8t2	sig	256	-----BEGIN RSA PRIVATE KEY-----\r\nMIIJKQIBAAKCAgEA747SHqYhaWkuCj0cDQGESZ/dUhalQcbaTNanhbu12kgVIplzNnugVdiK/poaG1B27XrrF+1AJdAdZ/3ReUWkOeSD9tdc7GbCQ0XQzoX8/MS8bUicuUJ8mLuSFFMIOM6XTg1Z08KBAQbVALgEmfgabZtaQsWRoJWg3pWKuAGzwqOzYm6RD/M1d88UuUSauJuoym9D2KBrl0bN2OaYChLifxHooMubjOm155UFnd1t/oukKioEjVkz4pxIoKJrpWF4b5gE6ei5I7Yzpy7XBa7Pv6MiG/Rss/h1ly94BgLskxA57uUfJthXjffJq5iKGs4f5UF9KZFdYM8JatKFNwSDGHa/ImyXMVPiITl9nxyZH1EJDuMkEbZ8ZQWJBv2s6ZCfi5jIq6K5sNn+ysIyTDXOyshNMbOSn7iwFjsx5cJDjcZdKuYVJnzOnj85sO6CpJZ32jk/QerFGRHGjokAN1bolnBY9101DexKOrRGW/i+H9bcVsUzWDRNnwjAYt1Nf3dp9muZ0G9uKE6Z3pzLjbmckL1bFuUAcdvi3EmqWl6BmLTQs0tLQe709Q2uLxqdpUeckM+40RJJeY+M4/bOqOpIZkyGy8d18LoKiZY03H/SpMskRvCc1yvEcRyuIoEPxT4uNHf4YV4Qed2LOov3qi4d8o0hyN2ZPlr99qMj41Af4NkCAwEAAQKCAgEAnPKsVSowr7gaUtjwnNDGk9nqDZMKmEqo0Ti9Lo/pt+YL+swgQKzEQhoKDn515jlUgYhLqDRnF57+9RfE+rgWvVsq3jkBB1zXn22JPRVpx005yjuNeo7FxOb28NvpghZP6PI0TNmc3UhVmw/0688xuWfTvfVk0JnXeJzu8lkjJb1MlIut/I4yFJmWkT8SQyqwblhxUebgNo9L4/RH3im7PNdF2rsq4SppZB0tPd1J6EAiwQEgVF8B8FDGAIAJGKQAXNRzO7CeQ3hm5Px6IZ4DPCGsAjakVVDN8cxGzWFzD3LNEegI/dE1o6yY8xSQPrmXCgNa9jXnwLpECDl+z6nkHImJZ1LwiW73uiwQ5Jnli5SAfQFEwRytUKbhKdo00TazyEtsZ5Z5Lbj5vHZR9gfiWL8so1cd57VRZRwlbOLVYow9Xu1q3ZGgpCM0RkzBfse09uDt20ooTNcNiAMjtZAuMEjf6l8wwOafUXjrQPRInlecHFlO2GNErChEci0HI51retxSD5oy2xf8ZKGkWloC8fIMY2qElOJtqTdWEDp8qiCEcpvX8feH28uOL5NqHP2piNd4+h6KIeeDVCa3hjMS+J1spShloz0AB78IjDO2f3UpW6PmRRKy7xIL5M1QHz0HvL09qnYszWTQsq5NArGGv9yu4yFvdAoKqchvz/3nrRUCggEBAPdsE+sLITvJ1PhhUMMQLHc/kPyTjgvO4CKpHsJ6uxyTXogE4iaXSiYiESMe+tuxpTRVzzqf9qvQCpb8PxAauaxhwfdhMoXezhYdP6rEa2TRIhadoG8peht5sFhX5SThlqYaEUPYIdL9XJfKpp1AlrNISMhDPrCbXDUnAlpN1pyTS2qb1ZwhAAzWB9M7ubypcNlHR/07dXP+5PYB83VGrjrO3YV7EByDI61AqBoJzzpnzp6fwA0GSKpqzXGi4njHV5ze4VRYGorqLEDV8ewvsILBcw968Zdt2d/ahTFAZwgIT1HO3bXmikynG8T13TrUwuu9F4LQcZ5u+wun6QnrZucCggEBAPfc8iK/o8ybMpmhng3TZWWNmSZCqEc1HbDe3YhlmOA7bTrOZM65eIjgt5gJmm0KqoVC3oq1OH59nlg933RrRnWM5ioL0wa9yp3cZKqQFaPXXhakljVMPvHBPPxE5A5QqmeWbDyOpxJpn3PtRYtq0o/5jkfaIXSX+h4a/jvKOm/kwUq3KTQ4d3K2QmSy8I0JeKN/oFXBL4UYnuIX+00zCsjoZkJurv8AV8fWNhdfd67PHI+o7OqM2gQBELHgr/rolNDhwHs4bitWvFE5qz0LAYVbWipA77EKVE/PgGA38S91ZAyWeECJ7iAaaMZIDzkkgpYUGj8AvY9Li4yNTqjGQj8CggEBAMR1luM9NShKPMb0TrJ0dzpAyRkk+Nc7bxFWhEwcM9Ke2aLbbc8CtifNSRpAESS8y9bgg+mi9rS6Po5gwJpC/kd4YBHTpdBSeAVrOBCaYkPtI0od4zQhFQoX+ARN1m8QiRRfAnKCfWkRMKJ+kQmwLXkx3kjVzENjOTYjQWT/BXfSJUIDdvu/4FBQ6mm5tOOvDyIXzXuv6LUwIhGMvwnSE6oydAb3DnX1UzDQdCoou9k+b/vYESDGapCWuYaPtY/9iP3Qo87bHkhLZNQejTfjLh7FCF20W3zIBwYOd1ACOU1Re9oTjkxPQGVZE12zc/Sw2A1jWfXPGUiaCtDYhNwRhOUCggEACeivVWxL5BYgQ7wOUYct+o1angj0KUSaV0PRn25QWkaF61/s78bCZtZ1AIMBxXIztvghZXIxO/1Roz11/XV8b56eZPfsC8zymLUC4T65Xr9xZ35U8vSFX6zV/0/RvjDDXzjIQvOBAl9unHfT2+r9V/wmEAFMbRjWSvXRTBqdk3OVtqLz5r6LJ+7ZYKU2sKy8Qe0MP+FlQPDnCSrkRQXRXI7N58H9BPzChZ6usuiCJF7rSWL7dbUD0j0oqbPN1T4PFPqxczuiS+E/zg98JQiXmvk39ZB7BJzhGf+1piMWZUtQIKCzVgEtn+LuZV7kHOi0v8M1+WbSLTRb89aCWoTyiQKCAQA3GGC7zDBxxSj2rvPstAx0+7BkdSop8Lx57WRtJxe6YJcdk7AmWohbpLTXJzn/ttnU7t4qqYSPx2aKvzuROkBkYlqv8jsf8hffmpdHic2WMuJF6xnTM3mopoxNvCqjGQQsAQmvDVAsXq07CFXpMnQTumuDNPW/UiDw1QB5h0mob674yx+guUUCQlfGiCRHkrUZ/2DJGChTKaWMckFwsI5ArqsZZWyC7L40iKZdP3bwKiakF5Y62ZTqGvb6LLBM7pK6+s5q3Md7a7rUG0tPQC34w4iYle2cAa5pUEhj9tnoHHjT0W2HM8NMM82A8y8JghDn9m9oZGAgV4WcJyX7n8Ss\r\n-----END RSA PRIVATE KEY-----
\.


--
-- TOC entry 5742 (class 0 OID 134390)
-- Dependencies: 302
-- Data for Name: wps_gui_webprocessingservice; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.wps_gui_webprocessingservice (id, name, endpoint, username, password) FROM stdin;
-- 1	PyWPS_vforwater	https://portal.vforwater.de/demo/wps
\.


--
-- TOC entry 5744 (class 0 OID 134403)
-- Dependencies: 304
-- Data for Name: wps_gui_wpsresults; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.wps_gui_wpsresults (id, creation, access, open, outputs, wps, inputs) FROM stdin;
\.


--
-- TOC entry 5750 (class 0 OID 0)
-- Dependencies: 274
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- TOC entry 5751 (class 0 OID 0)
-- Dependencies: 276
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 5752 (class 0 OID 0)
-- Dependencies: 272
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 240, true);


--
-- TOC entry 5753 (class 0 OID 0)
-- Dependencies: 280
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- TOC entry 5754 (class 0 OID 0)
-- Dependencies: 257
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 6, true);


--
-- TOC entry 5755 (class 0 OID 0)
-- Dependencies: 278
-- Name: auth_user_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_user_id_seq1', 1, true);


--
-- TOC entry 5756 (class 0 OID 0)
-- Dependencies: 282
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 5757 (class 0 OID 0)
-- Dependencies: 296
-- Name: author_manage_accessrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_accessrequest_id_seq', 1, true);


--
-- TOC entry 5758 (class 0 OID 0)
-- Dependencies: 294
-- Name: author_manage_deletionrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_deletionrequest_id_seq', 1, false);


--
-- TOC entry 5759 (class 0 OID 0)
-- Dependencies: 286
-- Name: author_manage_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_profile_id_seq', 26, true);


--
-- TOC entry 5760 (class 0 OID 0)
-- Dependencies: 288
-- Name: author_manage_resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_resource_id_seq', 27, true);


--
-- TOC entry 5761 (class 0 OID 0)
-- Dependencies: 292
-- Name: author_manage_resource_maintainers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_resource_maintainers_id_seq', 1, true);


--
-- TOC entry 5762 (class 0 OID 0)
-- Dependencies: 298
-- Name: author_manage_resource_owners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_resource_owners_id_seq', 15, true);


--
-- TOC entry 5763 (class 0 OID 0)
-- Dependencies: 290
-- Name: author_manage_resource_readers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.author_manage_resource_readers_id_seq', 6, true);


--
-- TOC entry 5764 (class 0 OID 0)
-- Dependencies: 215
-- Name: datasource_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.datasource_types_id_seq', 3, true);


--
-- TOC entry 5765 (class 0 OID 0)
-- Dependencies: 221
-- Name: datasources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.datasources_id_seq', 19, true);


--
-- TOC entry 5766 (class 0 OID 0)
-- Dependencies: 239
-- Name: datatypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.datatypes_id_seq', 1000, true);


--
-- TOC entry 5767 (class 0 OID 0)
-- Dependencies: 226
-- Name: details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.details_id_seq', 70, true);


--
-- TOC entry 5768 (class 0 OID 0)
-- Dependencies: 258
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 5, false);


--
-- TOC entry 5769 (class 0 OID 0)
-- Dependencies: 284
-- Name: django_admin_log_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq1', 1, false);


--
-- TOC entry 5770 (class 0 OID 0)
-- Dependencies: 259
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 48, false);


--
-- TOC entry 5771 (class 0 OID 0)
-- Dependencies: 270
-- Name: django_content_type_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq1', 43, true);


--
-- TOC entry 5772 (class 0 OID 0)
-- Dependencies: 268
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- TOC entry 5773 (class 0 OID 0)
-- Dependencies: 223
-- Name: entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.entries_id_seq', 19, true);


--
-- TOC entry 5774 (class 0 OID 0)
-- Dependencies: 203
-- Name: entrygroup_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.entrygroup_types_id_seq', 2, true);


--
-- TOC entry 5775 (class 0 OID 0)
-- Dependencies: 217
-- Name: entrygroups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.entrygroups_id_seq', 1, false);


--
-- TOC entry 5776 (class 0 OID 0)
-- Dependencies: 261
-- Name: heron_upload_uploadedfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.heron_upload_uploadedfile_id_seq', 1, false);


--
-- TOC entry 5777 (class 0 OID 0)
-- Dependencies: 205
-- Name: keywords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.keywords_id_seq', 7946, true);


--
-- TOC entry 5778 (class 0 OID 0)
-- Dependencies: 211
-- Name: licenses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.licenses_id_seq', 3, true);


--
-- TOC entry 5779 (class 0 OID 0)
-- Dependencies: 245
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.logs_id_seq', 3, true);


--
-- TOC entry 5780 (class 0 OID 0)
-- Dependencies: 209
-- Name: person_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.person_roles_id_seq', 20, true);


--
-- TOC entry 5781 (class 0 OID 0)
-- Dependencies: 207
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.persons_id_seq', 2, true);


--
-- TOC entry 5782 (class 0 OID 0)
-- Dependencies: 243
-- Name: spatial_scales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.spatial_scales_id_seq', 1, false);


--
-- TOC entry 5783 (class 0 OID 0)
-- Dependencies: 241
-- Name: temporal_scales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.temporal_scales_id_seq', 17, true);


--
-- TOC entry 5784 (class 0 OID 0)
-- Dependencies: 237
-- Name: thesaurus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.thesaurus_id_seq', 1, false);


--
-- TOC entry 5785 (class 0 OID 0)
-- Dependencies: 213
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.units_id_seq', 115, true);


--
-- TOC entry 5786 (class 0 OID 0)
-- Dependencies: 219
-- Name: variables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.variables_id_seq', 14, true);


--
-- TOC entry 5787 (class 0 OID 0)
-- Dependencies: 264
-- Name: watts_rsp_authfailureresponse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.watts_rsp_authfailureresponse_id_seq', 1, false);


--
-- TOC entry 5788 (class 0 OID 0)
-- Dependencies: 266
-- Name: watts_rsp_authsuccessresponse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.watts_rsp_authsuccessresponse_id_seq', 52, true);


--
-- TOC entry 5789 (class 0 OID 0)
-- Dependencies: 301
-- Name: wps_gui_webprocessingservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.wps_gui_webprocessingservice_id_seq', 1, false);


--
-- TOC entry 5790 (class 0 OID 0)
-- Dependencies: 303
-- Name: wps_gui_wpsresults_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.wps_gui_wpsresults_id_seq', 808, true);


-- Completed on 2021-02-09 08:26:54 CET

--
-- PostgreSQL database dump complete
--

