import React, { useState, useEffect, useLayoutEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Images from "../images/imagejson";
import { confirmAlert } from 'react-confirm-alert'; // Import

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


import { faExclamationTriangle, faTriangleExclamation, faWarning } from "@fortawesome/free-solid-svg-icons";
let first = true;
export default function WebForm() {

  let list = []
  const [hide, setHide] = useState(true)
  const [screenstitles, setScreensTitle] = useState("");
  let navigate = useNavigate();
  let [screenlst, screenLst] = useState([]);
  const [txtscreendrpdown, textDrpDwn] = useState([]);
  const [radioscreendrpdown, radioDrpDwn] = useState([]);
  const [comboscreendrpdown, comboDrpDwn] = useState([]);
  let [screenlisttile, screenListTitle] = useState([]);
  let bool = false;
  let screenJson = {}
  let data =JSON.parse(JSON.parse(sessionStorage['processdata']))
  // var data = require("./json.json");


  console.log(data)
  let [errorstr, setError] = useState("Screen ")
  let [screencount, screenCount] = useState(data["NOOFSCREENS"]);
  console.log(screencount);

  const saveScreenTitle = () => {
    
    let projectTitle = document.getElementById("projecttitle").value;
    sessionStorage.setItem("Project Title", projectTitle);
    sessionStorage.setItem("Screen Details", JSON.stringify(screenJson));
    sessionStorage.setItem("No Of Screen", screencount);
    navigate("/webformdetails")
  }
  const setScreensFunc = (valueotext, event) => {
    let a = document.getElementsByClassName("screen");
  };
  const preCheck = () => {
    screenJson = {}

    let allTextBoxes = document.getElementsByTagName('input');
    for (let i = 2; i < allTextBoxes.length; i++) {
      if (allTextBoxes[i].type == 'text') {
        let textboxvalue = allTextBoxes[i].value;
        if (typeof textboxvalue == "string" && textboxvalue.indexOf(',') > -1) {
          list.push(i - 1)
        }
        else {
          screenJson["Screen".concat(i - 1)] = textboxvalue
        }
      }
    }
    if (list.length > 0) {

    }
    return list;
  }

  let submit = () => {
    let list = preCheck();
    if (list.length > 0) {
      let alert = 0;
      showAlert();
    }
    else {
      confirmAlert({
        customUI: ({ onClose }) => {
          return (
            <div className='custom-ui shadow-lg p-3 mb-5 bg-white rounded'>
              <div className="row">
                <div className="col-md-2">


                  <FontAwesomeIcon className="warningicon" icon={faWarning} />
                </div>
                <div className="col-md-10 msgcontent">

                  <h1>Are you Sure about screen details?</h1>
                  <p className="pmsg">You cant change the title of screens in next steps. <br /> Please make sure your screen titles.</p>

                </div>
                <div className="buttonsec">
                  <button className="btn btn-primary btn-sm msgbtn" onClick={onClose}>No</button>
                  <button className="btn btn-primary btn-sm msgbtn"
                    onClick={() => {
                      saveScreenTitle()
                      onClose();
                    }}
                  >
                    Yes, Continue!
                  </button>
                </div>

              </div>

            </div>
          );
        }
      });


    }

  };


  const firstTime = () => {
    for (let i = 0; i < screencount; i++) {
      screenlisttile.push(data["SCREENS"]["Screen" + (i + 1).toString()][0]);

      screenlst.push(
        <div className="col-md-4">
          <div className="screen"></div>
          <input
            id={"textboxes".concat(i)}
            className="mt-3 form-control form-control-sm"
            type="text"
            placeholder=".form-control-sm"
            defaultValue={data["SCREENS"]["Screen" + (i + 1).toString()]}
            onChange={setScreensFunc(screenlisttile[i])}
          />
        </div>
      );
    }
  };

  if (first) {
    firstTime();
    first = false;
  }




  const onChange = (event) => {
    screenCount(event.target.value);
  };
  const back = () => {
    navigate("/userstory");
  };

  const addScreen = () => {
    screenCount(screencount + 1);
    screenlst.push(
      <div className="col-md-4">
        <div className="screen"></div>
        <input
          id={"textboxes".concat(screencount)}
          className="mt-3 form-control form-control-sm"
          type="text"
          placeholder=".form-control-sm"
      
        />
      </div>
    )
    console.log(screenlst)
    screenLst(screenlst)
  };
  const minusScreen = () => {
    if (screencount > 1) {
      screenCount(screencount - 1);
      screenlst.pop();
    } else {
      screenCount(1);
    }
  };
  let showAlert = () => {
    setError("Screen ");
    let error = document.getElementById('error').classList;

    if (error.contains("show")) {
      error.remove('show');
      error.add('collapse');
    }
    else if (error.contains("collapse")) {

      error.remove('collapse');
      for (let i = 0; i < list.length; i++) {
        errorstr = errorstr.concat(list[i].toString().concat(', '))
      }
      errorstr = errorstr.concat("have multiple titles. Each screen must have only one title please correct them!")
      console.log(errorstr)
      setError(errorstr)
      error.add('show');
      setTimeout(showAlert, 5000)
    }
  }

  // let items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"];

  // items.forEach((item, index) => {
  //   itemList.push(<li key={index}>{item}</li>);
  // });
  return (
    <>

      {bool}

      <div id='error' className="alert alert-danger collapse animate__animated animate__fadeInUp" role="alert">
        <div className="container-fluid">

          <FontAwesomeIcon className="erroricon" icon={faExclamationTriangle} />{errorstr}
        </div>
      </div>



      <Navbar title="PRO-VISION" profileID={1426363} user="Kevin Smith" />
      <div className="container webformcontainer">
        <h2 className="h2headingplan text-center">
          <span className="fontblue"> Digital is new Default. </span> Every
          thing happens on screen
        </h2>
        <div className="inner text-left">
          <div className="row">
            <div className="col-md-2">
              <div className="flex">
                <img src={Images.home.leftimage} alt="" />
              </div>
            </div>
            <div className="col-md-7">
              <div className="relativerectangle">
                <div className="mainformcard rounded-left shadow-lg card px-0 pt-4 pb-0 mt-3 mb-3">
                  <div className="innerform">

                    {/* form start */}
                    <div className="innerformcomp1">
                      <div className="form-group">
                        <h5 className="h5form1"> Project Title </h5>
                        <input
                          className="shadow p-3 form-control"
                          type="text"
                          id="projecttitle"
                          value={data["TITLE"]}
                          placeholder="Default input"
                        />
                      </div>
                    </div>
                    <div className="innerformcomp2">
                      <div className="row">
                        <div className="col-md-6">
                          <h5 className="h5form1"> No.of Screens </h5>
                        </div>
                        <div className="col-md-6 text-right">
                          <div className="number">
                            <button className="minus" onClick={minusScreen}>
                              -
                            </button>
                            <input
                              className="counterinput"
                              type="text"
                              value={screencount}
                              onChange={onChange}
                              disabled={true}
                            />
                            <span className="plus" onClick={addScreen}>
                              +
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="innerformcomp1">
                      <div className="screenvisual">
                        <div className="row"> {screenlst} </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
              {/* <div className="rectangleimg">
                              <img src={Images.home.rectangle} alt="" />
                            </div> */}
            </div>
            <div className="col-md-3">
              <div className="flex">
                <img src={Images.home.rightimage} alt="" />
              </div>
            </div>
          </div>
        </div>
        <div className="buttongroups">
          <div className="row">
            <div className="col-md-6"> </div>
            <div className="col-md-6">
              <div className="row">
                <div className="col-md-6">
                  <button
                    type="button"
                    onClick={back}
                    className="btn btn-outline-primary"
                  >
                    Back
                  </button>
                </div>
                <div className="col-md-6">
                  <button
                    onClick={submit}
                    type="button"
                    className="btn btn-primary"
                  >
                    Save and Continue
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <img className="cloud" src={Images.home.cloud} alt="" />
    </>
  );
}
