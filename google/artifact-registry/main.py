from google.cloud import artifactregistry_v1beta2


def retain_lastest_five_versions(project_id, location, repository, package):
    client = artifactregistry_v1beta2.ArtifactRegistryClient()
    package_name = f"projects/{project_id}/locations/{location}/repositories/{repository}/packages/{package}"

    # 패키지 별 버전 정보 준비
    versions = client.list_versions(parent=package_name)

    version_dict = dict()

    for version in versions:
        version_dict[version.create_time] = version.name

    sorted_version_dict = dict(sorted(version_dict.items(), key=lambda item: item[0], reverse=True))

    if len(sorted_version_dict) > 5:
        # 태그 정보 가져오기. Pair of tag and version.
        tag_pager = client.list_tags(parent=package_name)

        tag_dict = dict()

        for tag in tag_pager:
            tag_dict[tag.version] = tag.name

        iter_cnt = 0
        for vs_ctime, vs_name in sorted_version_dict.items():
            print(vs_ctime)
            iter_cnt = iter_cnt + 1

            if iter_cnt > 5:
                # 1. 태그 제거
                client.delete_tag(name=tag_dict[vs_name])

                # 2. 버전 삭제
                operation = client.delete_version(name=vs_name)
                result = operation.result()
                print(result)
    else:
        print('5 개 이하 artifact 존재')


if __name__ == '__main__':
    PROJECT_ID = 'en-data-mart-dev-id-0128'
    LOCATION = 'asia-northeast3'  # e.g., 'us-central1'
    REPOSITORY = 'rtu-subsystem-docker-images'
    PACKAGE = 'device-manager-api'

    retain_lastest_five_versions(PROJECT_ID, LOCATION, REPOSITORY, PACKAGE)
