import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { logOut, getStatus } from "../api/auth";
import AppContext from "../context/appContext";
import { useTranslation } from "react-i18next";
import logo from "../assets/img/logo.svg"

const Header = () => {
    const { t } = useTranslation("Common")

    const { setModalShow, logged, setLogged } = useContext(AppContext);

    const onLogin = () => setModalShow(true);

    async function onLogout () {
        await logOut();
        await getStatus(setLogged);
    }

    return (
    <header className="header" role="banner">
        <nav className="navbar navbar-expand-md navbar-light bg-light">

            <Link className="navbar-brand" to="/">
                <img src={logo} alt="logo" />
            </Link>
            <button 
                className="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>

            <div
                className="collapse navbar-collapse justify-content-end"
                id="navbarSupportedContent"
            >
                <ul className="navbar-nav mr-5">
                    <li className="nav-item">
                        <a className="nav-link"
                            href={t("GitHubLink")}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            {t("GitHubLinkText")}
                        </a>
                    </li>
                    {logged &&
                    <li className="nav-item">
                        <Link className="nav-link" to="/" onClick={onLogout}>
                            {t("LogOutText")}
                        </Link>
                    </li>
                    }
                </ul>
                {!logged &&
                <button className="login-btn" onClick={onLogin}>
                    {t("LogInText")}
                </button>
                }
            </div>
        </ nav>
    </ header>
    )
}
export default Header