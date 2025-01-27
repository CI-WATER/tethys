import getpass
from github import Github
from github.GithubException import BadCredentialsException

# Requirements: pip install PyGithub
# Github token with Contents read/write permissions on all of the tethysplatform tutorial repositories

# Tethys Version to Tag For
tethys_version = "4.3"

# Tutorial repos ({<repo_name>: {<branch>: <tag_prefix>}}
tutorial_repos = {
    "tethysplatform/tethysapp-dam_inventory": {
        "beginner-solution": "beginner",
        "intermediate-solution": "intermediate",
        "advanced-solution": "advanced",
        "websocket-solution": "websocket",
        "quotas-solution": "quotas",
    },
    "tethysplatform/tethysapp-bokeh_tutorial": {
        "master": "solution",
    },
    "tethysplatform/tethysapp-dask_tutorial": {
        "master": "solution",
        "setup-scheduler-solution": "setup-scheduler-solution",
        "setup-views-solution": "setup-views-solution",
        "dask-delayed-solution": "dask-delayed-solution",
        "dask-distributed-solution": "dask-distributed-solution",
        "multiple-leaf-solution": "multiple-leaf-solution",
    },
    "tethysplatform/tethysapp-geoserver_app": {
        "master": "solution",
        "start-and-register-solution": "start-and-register-solution",
        "upload-shapefile-solution": "upload-shapefile-solution",
        "map-geoserver-solution": "map-geoserver-solution",
        "map-draw-solution": "map-draw-solution",
    },
    "tethysplatform/tethysapp-thredds_tutorial": {
        "new-app-project-solution": "new-app-project-solution",
        "thredds-service-solution": "thredds-service-solution",
        "plot-at-location-solution": "plot-at-location-solution",
        "visualize-leaflet-solution": "visualize-leaflet-solution",
    },
    "tethysplatform/tethysapp-earth_engine": {
        "new-app-project-solution": "new-app-project-solution",
        "dataset-controls-solution": "dataset-controls-solution",
        "dataset-controls-js-solution": "dataset-controls-js-solution",
        "map-view-solution": "map-view-solution",
        "vis-gee-layers-solution": "vis-gee-layers-solution",
        "plot-data-solution": "plot-data-solution",
        "home-page-solution": "home-page-solution",
        "about-page-solution": "about-page-solution",
        "file-upload-solution": "file-upload-solution",
        "clip-by-asset-solution": "clip-by-asset-solution",
        "rest-api-solution": "rest-api-solution",
        "prepare-publish-solution": "prepare-publish-solution",
    },
    "tethysplatform/tethys_portal_docker": {
        "dockerfile-solution": "dockerfile-solution",
        "salt-state-solution": "salt-state-solution",
        "docker-compose-solution": "docker-compose-solution",
    },
    "tethysplatform/tethysapp-postgis_app": {
        "main": "solution",
    },
    "tethysplatform/tethysapp-map_layout_tutorial": {
        "new-app-project-solution": "new-app-project-solution",
        "configure-map-layout-solution": "configure-map-layout-solution",
        "data-prep-solution": "data-prep-solution",
        "add-spatial-data-solution": "add-spatial-data-solution",
        "configure-data-plotting-solution": "configure-data-plotting-solution",
    },
}

if __name__ == "__main__":
    print(
        "Please provide an API token with write permissions on all of the tethysplatform tutorial repositories."
    )
    token = getpass.getpass("Token: ")
    try:
        g = Github(token)

        print(
            f"Creating tutorial solution tags for Tethys Platform {tethys_version}..."
        )

        for repo_name in tutorial_repos:
            repo = g.get_repo(repo_name)
            tags = repo.get_tags()
            all_tags = [t.name for t in tags]
            print(f"\n{repo.name}:")

            for branch_name in tutorial_repos[repo_name]:
                # Create new tag
                tag_prefix = tutorial_repos[repo_name][branch_name]
                new_tag_name = f"{tag_prefix}-{tethys_version}"

                # Skip if tag exists already
                if new_tag_name in all_tags:
                    print(f"    {new_tag_name} -> Already Exists")
                    continue

                branch = repo.get_branch(branch_name)
                print(f"    {new_tag_name} -> {branch.name} ({branch.commit.sha})")

                tag_title = tag_prefix.replace("-", " ").replace("_", " ").title()

                if "solution" in tag_title.lower():
                    tag_message = (
                        f"{tag_title} for Tethys Platform {tethys_version} Release."
                    )
                    release_name = f"{tag_title} - Tethys Platform {tethys_version}"
                else:
                    tag_message = f"{tag_title} Solution for Tethys Platform {tethys_version} Release."
                    release_name = (
                        f"{tag_title} Solution - Tethys Platform {tethys_version}"
                    )

                repo.create_git_tag_and_release(
                    tag=new_tag_name,
                    tag_message=tag_message,
                    release_name=release_name,
                    release_message="",
                    object=branch.commit.sha,
                    type="commit",
                )

    except BadCredentialsException:
        print(
            "Unable to authenticate with given token. Please check the token and try again."
        )
        exit(1)
