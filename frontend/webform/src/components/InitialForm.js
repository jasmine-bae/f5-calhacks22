import { Form } from "@quillforms/renderer-core";
import { useState } from 'react'
import "@quillforms/renderer-core/build-style/style.css";
import axios from "axios"
import { registerCoreBlocks } from "@quillforms/react-renderer-utils";
import { useFieldAnswer } from "@quillforms/renderer-core";
import "../styles.css";

registerCoreBlocks();
const InitialForm = () => {

  function sendURL(linkedin_URL, github_handle) {
    console.log(URL);
    axios({
      method: "POST",
      url: "/scrape",
      headers: {},
      data: {
        linkedin_url: linkedin_URL,
        github_handle: github_handle
      }
    });
  }
        
  return (
    <div style={{ width: "100%", height: "100vh" }}>
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
            },
            {
              name: "short-text",
              id: "abcd",
              attributes: {
                required: true,
                label: "Please enter your Github handle (no @)"
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
          sendURL(data.answers['abasd'].value, data.answers['abcd'].value);
        }}
      />
    </div>
  );
};

export default InitialForm;
