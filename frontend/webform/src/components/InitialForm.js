import { Form } from "@quillforms/renderer-core";
import { useState } from 'react'
import "@quillforms/renderer-core/build-style/style.css";
import axios from "axios"
import { registerCoreBlocks } from "@quillforms/react-renderer-utils";
import { useFieldAnswer } from "@quillforms/renderer-core";
import "../styles.css";

registerCoreBlocks();
const InitialForm = () => {
  const [profileData, setProfileData] = useState(null)

  const fieldAnswer = useFieldAnswer("bv91em9123");

  function getData() {
    axios({
      method: "GET",
      url: "/profile",
    })
    .then((response) => {
      const res = response.data
      setProfileData(({
        profile_name: res.name,
        about_me: res.about}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  function sendURL(URL) {
    console.log(URL);
    axios({
      method: "POST",
      url: "/scrape",
      headers: {},
      data: {
        url: URL
      }
    });
  }
        
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me: {profileData.about_me}</p>
            </div>}
      <Form
        formId="1"
        formObj={{
          blocks: [
            {
              name: "welcome-screen",
              id: "jg1401r",
              attributes: {
                label: "Welcome!",
                description: "Create your portfolio website in a few easy steps",
                attachment: {
                  type: "image",
                  url:
                    "https://quillforms.com/wp-content/uploads/2022/01/4207-ai-1.jpeg"
                }
              }
            },
            {
              name: "multiple-choice",
              id: "gqr1294c",
              attributes: {
                required: true,
                multiple: false,
                verticalAlign: false,
                label: "Which type of website portfolio do you want?",
                choices: [
                  {
                    label: "Developer",
                    value: "developer"
                  },
                  {
                    label: "Designer",
                    value: "designer"
                  },
                ]
              }
            },
            {
              name: "website",
              id: "abasd",
              attributes: {
                required: true,
                multiple: true,
                label: "Please insert your LinkedIn profile url!"
              }
            }
          ],
          settings: {
            animationDirection: "vertical",
            disableWheelSwiping: false,
            disableNavigationArrows: false,
            disableProgressBar: false
          },
          theme: {
            font: "Roboto",
            buttonsBgColor: "#9b51e0",
            logo: {
              src: ""
            },
            questionsColor: "#000",
            answersColor: "#0aa7c2",
            buttonsFontColor: "#fff",
            buttonsBorderRadius: 25,
            errorsFontColor: "#fff",
            errorsBgColor: "#f00",
            progressBarFillColor: "#000",
            progressBarBgColor: "#ccc"
          }
        }}
        onSubmit={(data, { completeForm, setIsSubmitting }) => {
          setTimeout(() => {
            setIsSubmitting(false);
            completeForm();
          }, 500);
          sendURL(data.answers['abasd'].value);
        }}
      />
    </div>
  );
};

export default InitialForm;
