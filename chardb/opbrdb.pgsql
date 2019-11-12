--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7
-- Dumped by pg_dump version 10.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
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


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: chars; Type: TABLE; Schema: public; Owner: blaz
--

CREATE TABLE public.chars (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    alias character varying(150) NOT NULL,
    elem character varying(10) NOT NULL,
    class character varying(10) NOT NULL,
    tot_pow smallint NOT NULL,
    hp smallint NOT NULL,
    atk smallint NOT NULL,
    def smallint NOT NULL,
    crit numeric(3,2) NOT NULL,
    char_trait text NOT NULL,
    trait_1 text NOT NULL,
    trait_2 text NOT NULL,
    f2p boolean NOT NULL,
    skl_a character varying(100) NOT NULL,
    skl_b character varying(100) NOT NULL,
    init_rarity numeric(1,0) NOT NULL,
    art character varying(100) NOT NULL,
    frag character varying(100)
);


ALTER TABLE public.chars OWNER TO blaz;

--
-- Name: chars_id_seq; Type: SEQUENCE; Schema: public; Owner: blaz
--

CREATE SEQUENCE public.chars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chars_id_seq OWNER TO blaz;

--
-- Name: chars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: blaz
--

ALTER SEQUENCE public.chars_id_seq OWNED BY public.chars.id;


--
-- Name: chars id; Type: DEFAULT; Schema: public; Owner: blaz
--

ALTER TABLE ONLY public.chars ALTER COLUMN id SET DEFAULT nextval('public.chars_id_seq'::regclass);


--
-- Data for Name: chars; Type: TABLE DATA; Schema: public; Owner: blaz
--

COPY public.chars (id, name, alias, elem, class, tot_pow, hp, atk, def, crit, char_trait, trait_1, trait_2, f2p, skl_a, skl_b, init_rarity, art, frag) FROM stdin;
2	Luffy	v1 Strawhats	Red	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/M8n8qWB/img-icon-luffy-orig01-skill-a.png	https://i.ibb.co/qjvf0mp/img-icon-luffy-orig01-skill-b.png	2	https://i.ibb.co/35KF0HL/img-chara-luffy-orig01-l.png	https://i.ibb.co/h9GCmv2/img-chara-luffy-orig01-pieces.png
4	Sanji	v1 Strawhats	Blue	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/ZVQssDq/img-icon-sanji-orig01-skill-a.png	https://i.ibb.co/3pnfcHZ/img-icon-sanji-orig01-skill-b.png	2	https://i.ibb.co/5Kqv0qd/img-chara-sanji-orig01-l.png	https://i.ibb.co/Hpjpwy3/img-chara-sanji-orig01-pieces.png
5	Usopp	v1 Strawhats	Blue	Runner	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/K944g0N/img-icon-usopp-orig01-skill-a.png	https://i.ibb.co/rpbn19x/img-icon-usopp-orig01-skill-b.png	2	https://i.ibb.co/gJ6nbLn/img-chara-usopp-orig01-l.png	https://i.ibb.co/0F3TwXV/img-chara-usopp-orig01-pieces.png
6	Zoro	v1 Strawhats	Green	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/j3jQ6nK/img-icon-zoro-orig01-skill-a.png	https://i.ibb.co/GPhbY3T/img-icon-zoro-orig01-skill-b.png	2	https://i.ibb.co/myFFBPY/img-chara-zoro-orig01-l.png	https://i.ibb.co/PQW8y4t/img-chara-zoro-orig01-pieces.png
7	Butchie	Starter	Blue	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/Q9Hqh7c/img-icon-butchie-orig01-skill-a.png	https://i.ibb.co/dfDntDJ/img-icon-butchie-orig01-skill-b.png	2	https://i.ibb.co/qMPfH4Y/img-chara-butchie-orig01-l.png	https://i.ibb.co/5jYV7yK/img-chara-butchie-orig01-pieces.png
9	Higuma	Starter	Red	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/hm45rmj/img-icon-higuma-orig01-skill-a.png	https://i.ibb.co/WvZ5k4R/img-icon-higuma-orig01-skill-b.png	2	https://i.ibb.co/FVsWxYj/img-chara-higuma-orig01-l.png	https://i.ibb.co/7kW2xQb/img-chara-higuma-orig01-pieces.png
10	Johnny	Starter	Blue	Runner	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/VtLzVCG/img-icon-johnny-orig01-skill-a.png	https://i.ibb.co/8rgqg28/img-icon-johnny-orig01-skill-b.png	2	https://i.ibb.co/sPzqRMh/img-chara-johnny-orig01-l.png	https://i.ibb.co/KwbN2jp/img-chara-johnny-orig01-pieces.png
11	Morgan	Starter	Blue	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/XDyXgVv/img-icon-morgan-orig01-skill-a.png	https://i.ibb.co/pJNbZFk/img-icon-morgan-orig01-skill-b.png	2	https://i.ibb.co/L8WhkhP/img-chara-morgan-orig01-l.png	https://i.ibb.co/tYN6b7R/img-chara-morgan-orig01-pieces.png
12	Yosaku	Starter	Red	Runner	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/LZQ4wPC/img-icon-yosaku-orig01-skill-a.png	https://i.ibb.co/qCVTC42/img-icon-yosaku-orig01-skill-b.png	2	https://i.ibb.co/FVv1CS3/img-chara-yosaku-orig01-l.png	https://i.ibb.co/RgrqhNX/img-chara-yosaku-orig01-pieces.png
14	Coby	Starter	Red	Defender	6148	4648	822	1171	0.11	NA	NA	NA	f	https://i.ibb.co/6YPnfvV/img-icon-coby-orig01-skill-a.png	https://i.ibb.co/W5Cb65h/img-icon-coby-orig01-skill-b.png	2	https://i.ibb.co/h8G84bf/img-chara-coby-orig01-l.png	https://i.ibb.co/z4ShC24/img-chara-coby-orig01-pieces.png
15	Nami	v1 Strawhats	Green	Runner	6149	4431	949	1108	0.11	NA	NA	NA	f	https://i.ibb.co/MZzgV7H/img-icon-nami-orig01-skill-a.png	https://i.ibb.co/YyFmy23/img-icon-nami-orig01-skill-b.png	2	https://i.ibb.co/d0YhD8W/img-chara-nami-orig01-l.png	https://i.ibb.co/FWwGL5D/img-chara-nami-orig01-pieces.png
16	Helmeppo	Starter	Green	Runner	6149	4688	931	1062	0.11	NA	NA	NA	f	https://i.ibb.co/jhcKybn/img-icon-helmeppo-orig01-skill-a.png	https://i.ibb.co/zmy6kDb/img-icon-helmeppo-orig01-skill-b.png	2	https://i.ibb.co/J3cHR2f/img-chara-helmeppo-orig01-l.png	https://i.ibb.co/phrKWxC/img-chara-helmeppo-orig01-pieces.png
17	Chopper	v1 Strawhats	Red	Runner	6348	4856	985	1214	0.11	NA	NA	NA	f	https://i.ibb.co/g6QpgbK/img-icon-chopper-orig01-skill-a.png	https://i.ibb.co/Kbh6Q2w/img-icon-chopper-orig01-skill-b.png	2	https://i.ibb.co/zG5WH5N/img-chara-chopper-orig01-l.png	https://i.ibb.co/P92ykVF/img-chara-chopper-orig01-pieces.png
18	Brook	v1 Strawhats	Green	Runner	6614	5289	1100	1323	0.11	NA	NA	NA	f	https://i.ibb.co/BNcLgWn/img-icon-brook-orig01-skill-a.png	https://i.ibb.co/Mp1NPRm/img-icon-brook-orig01-skill-b.png	2	https://i.ibb.co/2hZGQZP/img-chara-brook-orig01-l.png	https://i.ibb.co/9vfw6xW/img-chara-brook-orig01-pieces.png
19	Franky	v1 Strawhats	Red	Defender	6680	5585	1035	1397	0.11	NA	NA	NA	f	https://i.ibb.co/my2sbKP/img-icon-franky-orig01-skill-a.png	https://i.ibb.co/zPHRm9X/img-icon-franky-orig01-skill-b.png	2	https://i.ibb.co/gFcJ0pm/img-chara-franky-orig01-l.png	https://i.ibb.co/5rqXLSN/img-chara-franky-orig01-pieces.png
21	Don Krieg	Starter	Green	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/W0zMDkD/img-icon-donkrieg-orig01-skill-a.png	https://i.ibb.co/YWZyD96/img-icon-donkrieg-orig01-skill-b.png	3	https://i.ibb.co/yVfRKxB/img-chara-donkrieg-orig01-l.png	https://i.ibb.co/yVqhGQs/img-chara-donkrieg-orig01-pieces.png
22	Zeff	Starter	Red	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/QNb4Bws/img-icon-zeff-orig01-skill-a.png	https://i.ibb.co/GnXTQd5/img-icon-zeff-orig01-skill-b.png	3	https://i.ibb.co/fpnN1BM/img-chara-zeff-orig01-l.png	https://i.ibb.co/8dHYYn8/img-chara-zeff-orig01-pieces.png
23	Sanji	Alabasta : Veau Vengeance Sanji	Blue	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/SfCmxFy/img-icon-sanji-alab01-skill-a.png	https://i.ibb.co/F5sgxCR/img-icon-sanji-alab01-skill-b.png	3	https://i.ibb.co/YLdyR2z/img-chara-sanji-alab01-l.png	https://i.ibb.co/sQcLsC1/img-chara-sanji-alab01-pieces.png
25	Kuro	Starter	Green	Attacker	7131	4620	1286	1061	0.11	NA	NA	NA	f	https://i.ibb.co/nrQ4SPX/img-icon-kuro-orig01-skill-a.png	https://i.ibb.co/KyjmR72/img-icon-kuro-orig01-skill-b.png	3	https://i.ibb.co/yyWCfBy/img-chara-kuro-orig01-l.png	https://i.ibb.co/TYrwWxv/img-chara-kuro-orig01-pieces.png
26	Tashigi	Starter	Blue	Runner	7209	5068	1054	1267	0.11	NA	NA	NA	f	https://i.ibb.co/5683CWJ/img-icon-tashigi-orig01-skill-a.png	https://i.ibb.co/TTGB0sJ/img-icon-tashigi-orig01-skill-b.png	3	https://i.ibb.co/GQww8Cr/img-chara-tashigi-orig01-l.png	https://i.ibb.co/HxNXTsG/img-chara-tashigi-orig01-pieces.png
28	Kuroobi	Starter	Blue	Defender	7289	5325	985	1360	0.11	NA	NA	NA	f	https://i.ibb.co/GsmvfWy/img-icon-kuroobi-orig01-skill-a.png	https://i.ibb.co/ZSWtcVN/img-icon-kuroobi-orig01-skill-b.png	3	https://i.ibb.co/Y7BP1tL/img-chara-kuroobi-orig01-l.png	https://i.ibb.co/XttRGj0/img-chara-kuroobi-orig01-pieces.png
29	Gin	Starter	Red	Attacker	7289	4929	1311	1133	0.11	NA	NA	NA	f	https://i.ibb.co/jgs7M2D/img-icon-gin-orig01-skill-a.png	https://i.ibb.co/VqXXXGN/img-icon-gin-orig01-skill-b.png	3	https://i.ibb.co/nMPGqFz/img-chara-gin-orig01-l.png	https://i.ibb.co/xfhKNKy/img-chara-gin-orig01-pieces.png
30	Alvida	Slip-Slip Fruit Alvida	Green	Runner	7289	4	1281	1198	0.11	NA	NA	NA	f	https://i.ibb.co/sqDyqSr/img-icon-alvida-sube01-skill-a.png	https://i.ibb.co/rbd55dT/img-icon-alvida-sube01-skill-b.png	3	https://i.ibb.co/n1ZqR2p/img-chara-alvida-sube01-l.png	https://i.ibb.co/3Tt9Qfv/img-chara-alvida-sube01-pieces.png
31	Usopp	Alabasta : 5t Hammer Usopp	Blue	Attacker	7289	5073	1266	1142	0.11	NA	NA	NA	f	https://i.ibb.co/2y2c6HS/img-icon-usopp-alab01-skill-a.png	https://i.ibb.co/6HdV3BW/img-icon-usopp-alab01-skill-b.png	3	https://i.ibb.co/Sxf5D6M/img-chara-usopp-alab01-l.png	https://i.ibb.co/PxknZZz/img-chara-usopp-alab01-pieces.png
32	Hatchan	Starter	Red	Attacker	7366	5008	1332	1179	0.11	NA	NA	NA	f	https://i.ibb.co/hHPNJb7/img-icon-hachi-orig01-skill-a.png	https://i.ibb.co/d0tzTj0/img-icon-hachi-orig01-skill-b.png	3	https://i.ibb.co/6YsNSkV/img-chara-hachi-orig01-l.png	https://i.ibb.co/BLJRRzZ/img-chara-hachi-orig01-pieces.png
33	Buggy	Buggy Pirates / Captain : Buggy	Red	Runner	7446	5477	1112	1370	0.11	NA	NA	NA	f	https://i.ibb.co/0rrHSLS/img-icon-buggy-orig01-skill-a.png	https://i.ibb.co/4WZhQFZ/img-icon-buggy-orig01-skill-b.png	3	https://i.ibb.co/dQzhGgd/img-chara-buggy-orig01-l.png	https://i.ibb.co/rm81CYj/img-chara-buggy-orig01-pieces.png
34	Shanks	Red-Haired Pirates / Captain : Shanks	Red	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/0jX2f5x/img-icon-shanks-orig01-skill-a.png	https://i.ibb.co/64QTZWR/img-icon-shanks-orig01-skill-b.png	4	https://i.ibb.co/Bj05LNy/img-chara-shanks-orig01-l.png	https://i.ibb.co/D7rjg4m/img-chara-shanks-orig01-pieces.png
36	Vivi	Alabasta: Peackock Slahser Nefetari Vivi	Green	Runner	8466	5917	1285	1480	0.11	NA	When using Skill 1: Boosts SPD by 10% for 20s (Cannot Stack)	When your team has less treasure secured: Boost the cooldown reduction speed of dodge by 50%	f	https://i.ibb.co/xgzrMW5/img-icon-vivi-alab01-skill-a.png	https://i.ibb.co/NVRM7Sb/img-icon-vivi-alab01-skill-b.png	4	https://i.ibb.co/PxRwC32/img-chara-vivi-alab01-l.png	https://i.ibb.co/BG6HpSQ/img-chara-vivi-alab01-pieces.png
37	Yasopp	Red-Haired Pirates / Sharp Shooter : Yasopp	Green	Runner	8741	6322	1422	1517	0.11	NA	around you captured treasure: reduce damage received by 30%.	When respawned boost SPD by 10% for 20S	f	https://i.ibb.co/y0CLsqY/img-icon-yasopp-orig01-skill-a.png	https://i.ibb.co/HKyT79n/img-icon-yasopp-orig01-skill-b.png	4	https://i.ibb.co/CPRKvJQ/img-chara-yasopp-orig01-l.png	https://i.ibb.co/wJzxd1Z/img-chara-yasopp-orig01-pieces.png
38	Arlong	Arlong Pirates / Captain : Arlong	Blue	Attacker	8741	6190	1578	1394	0.11	NA	around your enemy's treasure: increase damage dealt by 30%.	When you KO opponent: Boosts CRIT by 300%. 20 S	f	https://i.ibb.co/LnfHQCd/img-icon-arlong-orig01-skill-a.png	https://i.ibb.co/0Qrqb0T/img-icon-arlong-orig01-skill-b.png	4	https://i.ibb.co/ByKbxg1/img-chara-arlong-orig01-l.png	https://i.ibb.co/Sx3n8f4/img-chara-arlong-orig01-pieces.png
40	Mihawk	The Seven Warlords of the Sea : Dracule Mihawk	Red	Attacker	8796	6594	1610	1316	0.11	NA	around your enemy's treasure: increase damage dealt by 30%.	When there are 60s or less remaining: boosts crit by 300%. 20s	f	https://i.ibb.co/QY8y6LQ/img-icon-mihawk-orig01-skill-a.png	https://i.ibb.co/VMMhqvf/img-icon-mihawk-orig01-skill-b.png	4	https://i.ibb.co/MM348bj/img-chara-mihawk-orig01-l.png	https://i.ibb.co/yNxK18f/img-chara-mihawk-orig01-pieces.png
41	Smoker	Navy HQ Captain Smoker	Green	Defender	8796	6615	1235	1686	0.11	15% chance to: Reduce damage received by 30%	around your treasure: reduce damage by 30%	When respawned boost SPD by 10% for 20S	f	https://i.ibb.co/CK0SGdp/img-icon-smoker-orig01-skill-a.png	https://i.ibb.co/vZ7wkwH/img-icon-smoker-orig01-skill-b.png	4	https://i.ibb.co/YRKzf4B/img-chara-smoker-orig01-l.png	https://i.ibb.co/2F3B334/img-chara-smoker-orig01-pieces.png
42	Wapol	Drum Kingdom / Former Ruler : Wapol	Green	Defender	8796	6570	1190	1742	0.11	NA	around your treasure: reduce damage by 30%.	 When respawned boost SPD by 10% for 20S	f	https://i.ibb.co/1TmQt17/img-icon-wapol-orig01-skill-a.png	https://i.ibb.co/kgQbyvX/img-icon-wapol-orig01-skill-b.png	4	https://i.ibb.co/ysqx8Z6/img-chara-wapol-orig01-l.png	https://i.ibb.co/1T6Rm3F/img-chara-wapol-orig01-pieces.png
44	Enel	Kami Eneru	Green	Attacker	8833	6463	1493	1503	0.11	10% chance to:reduce damage received by 30%. 2% chance to: dodge without taking damage or it's effect. 3% chance to inflict shock. Nullify shock.	around your enemy's treasure: increase damage dealt by 30%.	When Respawned boost spd by 10%, 20s	f	https://i.ibb.co/F36MhQ0/img-icon-enel-orig01-skill-a.png	https://i.ibb.co/D44B4gN/img-icon-enel-orig01-skill-b.png	4	https://i.ibb.co/tKmJmtf/img-chara-enel-orig01-l.png	https://i.ibb.co/8XRksDF/img-chara-enel-orig01-pieces.png
45	Crocodile	The Seven Warlords of the Sea : Crocodile	Blue	Defender	8870	6522	1369	1649	0.11	15% chance to: Reduce damage received by 30%	around your captured Treasure: increase damage dealt by 30%	When you KO an opponent: Recover hp by 15%	f	https://i.ibb.co/yfGP9ZH/img-icon-sircrocodile-orig01-skill-a.png	https://i.ibb.co/w0ndTTM/img-icon-sircrocodile-orig01-skill-b.png	4	https://i.ibb.co/YT5GzGM/img-chara-sircrocodile-orig01-l.png	https://i.ibb.co/ZBrWbqm/img-chara-sircrocodile-orig01-pieces.png
46	Akainu	Navy HQ Admiral Akainu [Sakazuki]	Red	Attacker	8925	6604	1645	1408	0.11	15% chance to: Reduce damage received by 30%. Nullify aflame. When critical occurs, inflict long aflame	Around your enemy's treasure: increase damage dealt by 30%. When health over 80% resist stagger effect.	When your team has more treasure, boost cooldown reduction speed of skill 1 by 50%. When health is less than 30%, reduce damage received by 20%	f	https://i.ibb.co/hRG6h4w/img-icon-akainu-orig01-skill-a.png	https://i.ibb.co/D55KfzH/img-icon-akainu-orig01-skill-b.png	4	https://i.ibb.co/ZXCj2pC/img-chara-akainu-orig01-l.png	https://i.ibb.co/1ssYFNY/img-chara-akainu-orig01-pieces.png
47	Luffy	Alabasta : Gum Gum Storm Luffy	Red	Defender	8925	6490	1458	1623	0.11	Nullify shock	When in area around your captured tresure: Reduce damage recived by 30%	When your Strength is less than 30%: Boost CRIT by 300% for 20s (Cannot Stack)	f	https://i.ibb.co/ypSSqfg/img-icon-luffy-alab01-skill-a.png	https://i.ibb.co/pJ79Bqw/img-icon-luffy-alab01-skill-b.png	4	https://i.ibb.co/6bBVLv2/img-chara-luffy-alab01-l.png	https://i.ibb.co/7WVhGnL/img-chara-luffy-alab01-pieces.png
39	Luffy	30 Million Berry Bounty : Monkey D. Luffy	Red	Attacker	8741	6099	1580	1415	0.11	Nullify shock	around your enemy's treasure: increase damage dealt by 30%.	When your team has less treasure secured: boost the cooldown reduction speed of dodge by 50%.	f	https://i.ibb.co/ZKX6Qf0/img-icon-luffy-nost01-skill-a.png	https://i.ibb.co/gSTYR1m/img-icon-luffy-nost01-skill-b.png	4	https://i.ibb.co/JdzyZTW/img-chara-luffy-nost01-l.png	https://i.ibb.co/tb5cr4T/img-chara-luffy-nost01-pieces.png
49	Whitebeard	White Beard Pirates / Captain Whitebeard : Edward Newgate	Red	Defender	9016	6696	1447	1674	0.11	15% chance to: Reduce damage received by 30% + Reduce freeze time by 50% + Nullify tremor	around your treasure: reduce damage by 30%	When your hp is less than 30% boost CRIT by 300% for 20s	f	https://i.ibb.co/LCLQYyq/img-icon-whitebeard-orig01-skill-a.png	https://i.ibb.co/LgxZwsb/img-icon-whitebeard-orig01-skill-b.png	4	https://i.ibb.co/603GsP5/img-chara-whitebeard-orig01-l.png	https://i.ibb.co/ZBjbpVP/img-chara-whitebeard-orig01-pieces.png
50	Zoro	One-Sword Slyle Iai Lion Song	Green	Attacker	0	0	0	0	0.11	When your allies are near the Treasure area where you are at: Boost the cooldown reduction speed of Skill 1 by 50%	When your Strength is less than 30%: Boosts CRIT by 300% for 20s (Cannot Stack)	NA	t	https://i.ibb.co/0BKvxR9/img-icon-zoro-alab01-skill-a.png	https://i.ibb.co/DDnxwnC/img-icon-zoro-alab01-skill-b.png	3	https://i.ibb.co/qMry2r4/img-chara-zoro-alab01-l.png	https://i.ibb.co/hmLVzkw/img-chara-zoro-alab01-pieces.png
3	Robin	v1 Strawhats	Green	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/1z0kBmW/img-icon-robin-skyp01-skill-a.png	https://i.ibb.co/9hNT3CW/img-icon-robin-skyp01-skill-b.png	2	https://i.ibb.co/VLdX9kp/img-chara-robin-skyp01-l.png	https://i.ibb.co/kM6D072/img-chara-robin-skyp01-pieces.png
8	Django	Starter	Red	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/VjdmvRD/img-icon-django-orig01-skill-a.png	https://i.ibb.co/CMF45Ym/img-icon-django-orig01-skill-b.png	2	https://i.ibb.co/LrfxKyz/img-chara-django-orig01-l.png	https://i.ibb.co/0s0CXy9/img-chara-django-orig01-pieces.png
13	Alvida	Alvida Pirates / Captain Alvida (Fat Alvida)	Green	Defender	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/KrLyyrj/img-icon-alvida-orig01-skill-a.png	https://i.ibb.co/7zTvhLC/img-icon-alvida-orig01-skill-b.png	2	https://i.ibb.co/JB2SCvd/img-chara-alvida-orig01-l.png	https://i.ibb.co/1sxpKqB/img-chara-alvida-orig01-pieces.png
20	Choo	Starter	Green	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/k6mxHVK/img-icon-choo-orig01-skill-a.png	https://i.ibb.co/0tbQZSK/img-icon-choo-orig01-skill-b.png	3	https://i.ibb.co/F7YphHP/img-chara-choo-orig01-l.png	https://i.ibb.co/tLMt9Vx/img-chara-choo-orig01-pieces.png
24	Nami	Alabasta : Climate Baton Nami	Green	Attacker	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/wWymKcy/img-icon-nami-alab01-skill-a.png	https://i.ibb.co/HzrnwMs/img-icon-nami-alab01-skill-b.png	3	https://i.ibb.co/fGwBn3Q/img-chara-nami-alab01-l.png	https://i.ibb.co/k2rnJTS/img-chara-nami-alab01-pieces.png
27	Vivi	Miss Wednesday	Blue	Runner	7209	5068	1054	1267	0.11	NA	When in the area around your captured treasure: Reduce damage recieved by 30%	When you capture the Treasure: Reduce the cooldown time of skill 1 by 30%. When dealing damage to an enemy inflicted with confuce: Increase damage dealt by 20%	f	https://i.ibb.co/12x4Nxj/img-icon-vivi-orig01-skill-a.png	https://i.ibb.co/1MKT5Cz/img-icon-vivi-orig01-skill-b.png	3	https://i.ibb.co/cQPzDYH/img-chara-vivi-orig01-l.png	https://i.ibb.co/8XM30Dx/img-chara-vivi-orig01-pieces.png
35	Kaya	Girl From Syrup Village : Kaya	Blue	Defender	8190	5593	1044	1526	0.11	NA	When your team has less treasure secured: boost the cooldown reduction speed of skill 1 by 50%	When a character from your team is KO'd: Increase team Boost gauge by 3%.	f	https://i.ibb.co/vvR2SVR/img-icon-kaya-orig01-skill-a.png	https://i.ibb.co/N6F2F0s/img-icon-kaya-orig01-skill-b.png	4	https://i.ibb.co/5x9XsP8/img-chara-kaya-orig01-l.png	https://i.ibb.co/Kw7nj1W/img-chara-kaya-orig01-pieces.png
43	Ace	White Beard Pirates / 2nd Division Commander : Portgaz D. Ace	Blue	Attacker	8833	6411	1615	1394	0.11	15% chance to: Reduce damage received by 30% + Nullify aflame	around your enemy's treasure: increase damage dealt by 30%.	When there are 60s or less remaining: boosts crit by 300%. 20s	f	https://i.ibb.co/8rHLhmn/img-icon-ace-orig01-skill-b.png	https://i.ibb.co/MVbfVQb/img-icon-ace-orig01-skill-a.png	4	https://i.ibb.co/vVGn63n/img-chara-ace-orig01-l.png	https://i.ibb.co/s1tbH5h/img-chara-ace-orig01-pieces.png
1	Cabaji	Starter	Green	Runner	0	0	0	0	0.11	NA	NA	NA	f	https://i.ibb.co/Bs3vcMc/img-icon-cabaji-orig01-skill-a.png	https://i.ibb.co/TT8s1zk/img-icon-cabaji-orig01-skill-b.png	2	https://i.ibb.co/KyxNw9X/img-chara-cabaji-orig01-l.png	https://i.ibb.co/YdfjJKQ/img-chara-cabaji-orig01-pieces.png
48	Aokiji	Navy HQ Admiral Aokiji [Kuzan]	Blue	Defender	8980	6608	1424	1683	0.11	10% chance to: Reduce damage by 30%. 5% Chance to: inflict freeze. Nullify Freeze	When in area around your captured tresure: Reduce damage recived by 30%. 120 seconds or more increase treasure gauge recovery.	When team has more treasure than enemy, boost cooldown of Skill 1 by 50%. When inflicting damage to enemy with freeze, increase damage by 20%	f	https://i.ibb.co/rQNqHCM/img-icon-aokiji-orig01-skill-a.png	https://i.ibb.co/8dGgxs6/img-icon-aokiji-orig01-skill-b.png	4	https://i.ibb.co/nnxKVBn/img-chara-aokiji-orig01-l.png	https://i.ibb.co/Gt6TNZg/img-chara-aokiji-orig01-pieces.png
\.


--
-- Name: chars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: blaz
--

SELECT pg_catalog.setval('public.chars_id_seq', 51, true);


--
-- Name: chars chars_pkey; Type: CONSTRAINT; Schema: public; Owner: blaz
--

ALTER TABLE ONLY public.chars
    ADD CONSTRAINT chars_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

