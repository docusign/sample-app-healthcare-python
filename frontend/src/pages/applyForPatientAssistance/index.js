import React, { useState, useEffect, useContext } from "react";
import AppContext from "../../context/appContext";
import { useTranslation } from "react-i18next";
import { useNavigate, useLocation } from "react-router-dom";
import InputText from "../../components/inputText";
import InputEmail from "../../components/inputEmail";
import SeeMore from "../../components/seeMore";
import ExtensionsModal from "../../components/extensionModal";
import { getExtensions, sendRequest } from "../../api/healthcareAPI";
import { getStatus } from "../../api/auth";

const urlPath = "/apply-for-patient-assistance";
const extensionsUrlPath = "/extensions";
const returnUrl = process.env.REACT_APP_DS_RETURN_URL + "/success?1";

const ApplyForPatientAssistance = props => {
    let navigate = useNavigate();

    const { t: tCommon } = useTranslation("Common");
    const { t } = useTranslation("ApplyForPatientAssistance");

    const [ submitted, setSubmitted ] = useState(false);
    const [ formError, setFormError ] = useState([true, true, true]);
    const [ apiError, setApiError ] = useState("");
    const [ response, setResponse ] = useState(null);
    const [ areExtensionsPresent, setAreExtensionsPresent ] = useState(false);
    const [ showModal, setShowModal ] = useState(false);

    const { setBackdrop, logged, setLogged } = useContext(AppContext);

    useEffect(() => {
        if (!logged) navigate("")
    }, )

    useEffect(() => {
        if (!response) {
            return;
        }

        window.DocuSign.loadDocuSign(response.client_id).then((docusign) => {
            const elem = document.getElementsByClassName("col form-holder mb-4")[0];
            elem.className = "col-sm-6";
            const signing = docusign.signing({
                url: response.view_url,
                displayFormat: "focused",
                style: {
                    branding: {
                        primaryButton: {
                            backgroundColor: "#9F289F",
                            color: "#fff",
                        },
                    },
                },
            });

            signing.on("sessionEnd", (_event) => {
                navigate("/success?1");
            });

            signing.mount("#agreement");
        });
    }, [response]);

    function isFormValid() {
        return formError.every(elem => elem === false)
    }

    async function handleSubmit (event) {
        event.preventDefault();

        getStatus(setLogged, navigate);
        setApiError("")

        // setSubmitted(true);
        if (!logged) navigate("")

        if (!isFormValid()) return;

        setBackdrop(true);
        const useWithoutExtension = sessionStorage.getItem("useWithoutExtension") === "true";
        const el = event.target.elements;
        const body = {
            first_name: el.FirstName.value,
            last_name: el.LastName.value,
            email: el.Email.value,
            return_url: returnUrl,
            useWithoutExtension,
        };

        try {
            if (!useWithoutExtension) {
                const extensions = await getExtensions(extensionsUrlPath);
                if(extensions.data?.areExtensionsPresent === false){
                    setAreExtensionsPresent(true);
                    setShowModal(true);
                    return;
                }
            }
            const response = await sendRequest(body, urlPath);
            setResponse(response.data);
        } catch (error) {
            setApiError(error.message)
        } finally {
            setBackdrop(false);
        }
    }

    return (
        <section className="content-section">
            <div className="container">
                {apiError &&
                    <div className="text-center">
                            <div className="alert alert-danger" role="alert">
                                {apiError}
                            </div>
                    </div>
                }
                <div className="row justify-content-center">
                    <div className="col form-holder mb-4">
                        <h4 className="card-title">{t("Title")}</h4>
                        {!response &&
                            <form onSubmit={handleSubmit}>
                                <InputText
                                    id="FirstName"
                                    label={t("FirstName")}
                                    errorText={t("ErrorText")}
                                    setFormError={setFormError}
                                    formError={formError}
                                    formErrorNum={0}
                                    submitted={submitted}
                                />
                                <InputText
                                    id="LastName"
                                    label={t("LastName")}
                                    errorText={t("ErrorText")}
                                    setFormError={setFormError}
                                    formError={formError}
                                    formErrorNum={1}
                                    submitted={submitted}
                                />
                                <InputEmail
                                    id="Email"
                                    label={t("Email")}
                                    warn={t("EmailWarn")}
                                    errorText={t("ErrorText")}
                                    setFormError={setFormError}
                                    formError={formError}
                                    formErrorNum={2}
                                    submitted={submitted}
                                />
                                <button className="h-card-button" type="submit">{t("ButtonName")}</button>
                            </form>
                        }
                        {response && <div style={{height: "600px"}} id="agreement"></div>}
                    </div>

                    <div className="w-100 d-block d-md-none"></div>

                    <SeeMore
                        title={t("SeeMore.Title")}
                        text={t("SeeMore.Text")}
                    />

                </div>
                {areExtensionsPresent && (
                    <ExtensionsModal
                        show={showModal}
                        onDownloadExtensions={
                            () => setShowModal(false)
                        }
                        onHide={
                            () => {
                                sessionStorage.setItem("useWithoutExtension", "true");
                                setShowModal(false);
                            }
                        }
                        title={tCommon("DownloadExtensionsHeader")}
                        message={tCommon("DownloadExtensionsMessage")}
                    />
                )}
            </div>
        </section>
    )
}
export default ApplyForPatientAssistance;