import React from "react";

import { Card, CardBody, CardText, Col, Button } from "reactstrap";

import { Fade } from "react-reveal";

const ProjectsCard = ({ data }) => {
	return (
		<Col lg="6">
			<Fade bottom duration={2000} >
				<Card className="shadow-lg--hover shadow mt-4">
					<CardBody>
						<img
							src={data.companylogo}
							style={{
								objectFit: "cover",
								left: 0,
								right: 0,
								top: "7rem",
								marginLeft: "auto",
								marginRight: "auto",
								width: "8rem",
								height: "8rem",
								borderRadius: "50%",
							}}
							className="shadow mb-3"
							alt={data.companylogo}
						/>
						<div className="d-flex px-3">
							<div className="pl-4">
								<h3>{data.name}</h3>
								<p className="description mt-3">{data.desc}</p>
								{data.github ? (
									<Button
										className="btn-icon"
										color="github"
										href={data.github}
										target="_blank"
										rel="noopener"
										aria-label="Github"
									>
										<span className="btn-inner--icon">
											<i className="fa fa-github" />
										</span>
									</Button>
								) : null}
								{data.link ? (
									<Button
										className="btn-icon"
										color="success"
										href={data.link}
										target="_blank"
										rel="noopener" aria-label="Twitter"
									>
										<span className="btn-inner--icon">
											<i className="fa fa-arrow-right mr-2" />
										</span>
										<span className="nav-link-inner--text ml-1">
											Demo
										</span>
									</Button>
								) : null}
							</div>
						</div>
						<CardText
							tag="div"
							className="description my-3 text-left"
						>
							<ul>
								{data.descBullets
									? data.descBullets.map((desc) => {
										return <li key={desc}>{desc}</li>;
									})
									: null}
							</ul>
						</CardText>
					</CardBody>
				</Card>
			</Fade>
		</Col>
	);
};

export default ProjectsCard;
