import emoji from "react-easy-emoji";

export const greetings = {
	name: "{{ name }}",
	title: "Hi all, I'm {{ name }}",
	description:
		"{{ cohere_desc }}",
};

export const openSource = {
	githubUserName: "{{ github }}",
};

export const contact = {};

export const socialLinks = {
	// url: "https://1hanzla100.github.io/",
	linkedin: "{{ linkedin_url }}",
	github: "https://github.com/{{github}}",
	// instagram: "https://www.instagram.com/__hanzla100",
	// facebook: "https://www.facebook.com/1hanzla100",
	// twitter: "https://twitter.com/1hanzla100",
};

export const SkillBars = [
	{% for skill in skill_prof %}
{
	Stack: "{{ skill.name }}", //Insert stack or technology you have experience in
		progressPercentage: {{ skill.proficiency }}, //Insert relative proficiency in percentage
},
{% endfor %}
];

export const educationInfo = [
	{% for edu in education %}
{
	schoolName: "{{ edu['school'] }}",
		subHeader: "{{ edu['degree'] }}",
			duration: "{{ edu['duration'] }}",
	},
{% endfor %}
];

export const experience = [
	{% for exp in jobs %}
{
	role: "{{ exp['title'] }}",
		company: "{{ exp['company'] }}",
			companylogo: "/img/icons/common/dusecaSoftware.jpg",
				date: "{{ exp['duration'] }}",
					descBullets: {{ exp['description'] }},
},
{% endfor %}
];

export const projects = [
	{% for proj in projects %}
{
	name: "{{ proj['name'] }}",
		descBullets: {{ proj['description'] }},
},
{% endfor %}
];

export const feedbacks = [
	{
		name: "John Smith",
		feedback:
			"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nisi, vel illo. Eum magnam beatae ratione eos natus accusamus unde pariatur fugiat at facilis, modi molestiae? Labore odio sit eligendi. Tenetur.",
	},
	{
		name: "John Smith",
		feedback:
			"Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nisi, vel illo. Eum magnam beatae ratione eos natus accusamus unde pariatur fugiat at facilis, modi molestiae? Labore odio sit eligendi. Tenetur.",
	},
];

// See object prototype on SEO.jsx page
export const seoData = {
	title: "{{ name }}",
	description:
		"A passionate Full Stack Web Developer and Blockchain Developer.",
	author: "{{ name }}",
	image: "https://avatars3.githubusercontent.com/u/59178380?v=4",
	url: "https://developer-portfolio-1hanzla100.vercel.app",
	keywords: [
		"Hanzla",
		"Hanzla Tauqeer",
		"@1hanzla100",
		"1hanzla100",
		"Portfolio",
		"Hanzla Portfolio ",
		"Hanzla Tauqeer Portfolio",
	],
}
