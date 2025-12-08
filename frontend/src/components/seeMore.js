import React from "react";
import parse from "html-react-parser";
import right_caret from "../assets/img/right_caret.png"
import down_caret from "../assets/img/down_caret.png"

const SeeMore = props => {
    const handleClick = (event) => {
        if(document.getElementById('seemore').getAttribute('aria-expanded') === "false"){
            document.getElementById("rightCaret").hidden = false
            document.getElementById("downCaret").hidden = true
        } else {
            document.getElementById("rightCaret").hidden = true
            document.getElementById("downCaret").hidden = false
        }
    };
    React.useEffect(() => {
        window.addEventListener('click', handleClick);
        return () => {
            window.removeEventListener('click', handleClick);
        };
    },[]);
    return (
        <div className="col bs-holder">
            <p>
                <a id="seemore" className="bs-link" data-bs-toggle="collapse" href="#collapseSeeMore" role="button" aria-expanded="false"
                    aria-controls="collapseSeeMore">
                    <img id='rightCaret' style={{'margin-right':'10px', 'margin-bottom':'5px'}} src={right_caret} alt='right caret' width='20' height='20'></img>
                    <img hidden id='downCaret' style={{'margin-right':'10px', 'margin-bottom':'5px'}} src={down_caret} alt='right caret' width='20' height='20'></img>
                    {props.title}
                </a>
            </p>
            <div className="collapse" id="collapseSeeMore">
                <div className="bs">
                    {parse(props.text)}
                </div>
            </div>
        </div>
    )
}
export default SeeMore;